import spacy
import pattern_patch
import checkForPassive.passiveCheck as passiveCheck
import analysePassiveConstruction.sentenceParser as analyseSentence
import verbConjugation.verbConjugator as verbConjugator
import composition.sentenceComposition as sentenceComposition
from langdetect import detect


# Load NLP model
try:
    nlp = spacy.load("en_core_web_lg")
except Exception as e:
    spacy.cli.download("en_core_web_lg")
    nlp = spacy.load("en_core_web_lg")


# Main Transformation Function
def passiveToActive(sentence, source):
    """
    This function takes a passive sentence as input and returns the active version of the sentence.

    Input: String inserted from the user

    Steps:
    1. Check if the sentence is English and passive
    2. For each identified passive construction:
        - Analyse the sentence
        - Conjugate the verb
        - Transform the sentence by combining the seperate parts
    3. Combine the active sentences into one sentence using the indices
    4. Return final active sentence

    Output: String with the active version of the sentence if the sentence is in English and passive, else an error message

    """
    activeSentences = {}
    activeSubclauses = {}
    oldSentences = {}
    newLengths = {}

    # check if the sentence is in English
    if detect(sentence) != "en":
        return "Sentence is not in English", {}

    sentence = sentence.strip()
    doc = nlp(sentence)

    # check if the is a passive construction in the sentence
    (
        identifiedPassiveSentences,
        preClause,
        postClause,
        indicesOfSubtrees,
    ) = passiveCheck.checkForPassive(doc)

    if identifiedPassiveSentences == []:
        return "\nNo passive construction identified", None
    else:
        # if passive constructions have been identified to the following steps for each identified passive construction
        for index, sentence in enumerate(identifiedPassiveSentences):
            try:
                passiveSentence = nlp(sentence.text)

                # analyse the sentence
                analysis_results = analyseSentence.analyseSentence(
                    passiveSentence, source
                )

                # conjugate the verb
                verbActive = verbConjugator.conjugateVerb(analysis_results)

                # transform the sentence by combining the seperate parts
                (
                    transformedSentence,
                    transformedSubclause,
                    newLength,
                ) = sentenceComposition.transformSentence(
                    analysis_results, verbActive, preClause[index], postClause[index]
                )

                # save the transformed sentence, the original sentence and the length of the new sentence for final composition later
                activeSentences[f"{indicesOfSubtrees[index]}"] = transformedSentence
                activeSubclauses[f"{indicesOfSubtrees[index]}"] = transformedSubclause
                oldSentences[f"{indicesOfSubtrees[index]}"] = sentence.text
                newLengths[f"{indicesOfSubtrees[index]}"] = newLength

            except Exception as e:
                print(f"An unexpected error occured during the conversion: {e}")
                raise

    try:
        # Sort the active sentences by the difference between the start and end index, so that the longest sentence is first and the shorter ones can be inserted into the longest (i.e. so the main sentence)
        def calc_diff(key):
            start, end = key.split(",")
            return int(end) - int(start)

        activeSentsSorted = dict(
            sorted(
                activeSentences.items(),
                key=lambda item: calc_diff(item[0]),
                reverse=True,
            )
        )
        # Combine the active sentences into one sentence using the indices
        indices_list = list(activeSentsSorted.keys())

        if len(indices_list) == 1:
            # If there is only one sentence, print and return it
            transformedSentence = activeSentsSorted[indices_list[0]] + ". "
            if source != "fileTransformation":
                print(f"\nPassive Sentence: {doc}")
                print(f"\nActive Sentence: {transformedSentence}")
                print("\n")
            return transformedSentence, activeSubclauses

        first_indices = indices_list[0]
        last_indices = indices_list[-1]

        # Get first and longest sentence, to insert other shorter subsentences into
        longest_sentence = " ".join(activeSentsSorted[first_indices].split())
        final_sentence = longest_sentence

        for current_indices in indices_list:
            # iterate through all the produced active sentences
            if current_indices == first_indices:
                continue

            # Get the start and end index of the current sentence
            start_index, end_index = map(int, current_indices.split(","))
            # Adapt the indices span according to the earlier transformations
            end_index = start_index + newLengths[current_indices]
            current_sentence = " ".join(activeSentsSorted[current_indices].split())
            current_sentence = nlp(current_sentence)

            # Get corresponding subclause from the original sentence
            oldSubclause = oldSentences[current_indices]
            if oldSubclause.endswith("."):
                oldSubclause = oldSubclause[:-1]

            newSubclause = current_sentence[start_index : end_index + 1]
            # newSubclause = [token.text for token in newSubclause]
            newSubclause = "".join(
                token.text + " "
                if token.text == ","
                else token.text_with_ws
                if not token.is_punct
                else token.text
                for token in newSubclause
            )
            if newSubclause.endswith(", "):
                newSubclause = newSubclause[:-2]

            # Replace the subclause with the passive construction in the original sentence with the new active subclause
            position = longest_sentence.find(oldSubclause)
            if position != -1:
                # If the subclause is found in the original sentence, replace it with the new active subclause

                modified_longest_sentence = (
                    longest_sentence[:position]
                    + newSubclause
                    + longest_sentence[position + len(oldSubclause) :]
                )
                longest_sentence = modified_longest_sentence
            final_sentence = longest_sentence

        final_sentence = final_sentence + ". "

        if source != "fileTransformation":
            print(f"Passive Sentence: {doc}")
            print(f"Active Sentence: {final_sentence}")
            print("\n")
    except Exception as e:
        print(
            f"The following error accured during the final composition of the active sentence: {e}"
        )
        raise

    return final_sentence, activeSubclauses
