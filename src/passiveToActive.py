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
        return "\n No passive construction identified", None
    else:
        # if passive constructions have been identified to the following steps for each identified passive construction
        for index, sentence in enumerate(identifiedPassiveSentences):
            try:
                passiveSentence = nlp(sentence.text)

                # analyse the sentence
                analysis_results = analyseSentence.analyseSentence(
                    passiveSentence, source
                )
                print(f"results: {analysis_results}")

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

                print("newLengths: ")
                print(newLengths)
                print("Old Sentences: ")
                print(oldSentences)
                print(indicesOfSubtrees)
                print("Active Sentences: ")
                print(activeSentences)
                print(f"Active Subsentence: {transformedSentence}")
                print(f"Active Subclause: {activeSubclauses}")

                print("-------------------------------------")
            except Exception as e:
                print(f"An unexpected error occured during the conversion: {e}")
                raise

    try:
        # Sort the active sentences by the difference between the start and end index, so that the shortest sentence is first and can be inserted into the longest so the main sentence
        def calc_diff(key):
            start, end = key.split(",")
            return int(end) - int(start)

        activeSentsSorted = dict(
            sorted(activeSentences.items(), key=lambda item: calc_diff(item[0]))
        )
        print("Sorted Active Sentences: ")
        print(activeSentsSorted)

        print("transformed active subclause")
        print(activeSubclauses)
        # Combine the active sentences into one sentence using the indices
        indices_list = list(activeSentsSorted.keys())
        if len(indices_list) == 1:
            # If there is only one sentence, print and return it
            transformedSentence = activeSentsSorted[indices_list[0]] + ". "
            print(f"Passive Sentence: {doc}")
            print(f"Active Sentence: {transformedSentence}")
            print("\n")
            return transformedSentence, activeSubclauses

        last_indices = indices_list[-1]

        # Get last and longest sentence, to insert other shorter subsentences into
        last_sentence = " ".join(activeSentsSorted[last_indices].split())

        for current_indices in indices_list:
            # iterate through all the produced active sentences
            if current_indices == last_indices:
                break

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

            print("old subclause")
            print(oldSubclause)
            print("current sentence: ")
            print(activeSentsSorted[current_indices])

            newSubclause = current_sentence[start_index : end_index + 1]
            newSubclause = [token.text for token in newSubclause]
            newSubclause = " ".join(newSubclause).strip()

            print("current_indices")
            print("start_index: ", start_index)
            print("end_index: ", end_index)
            print(current_indices)
            print("new clause")
            print(newSubclause)

            # Replace the subclause with the passive construction in the original sentence with the new active subclause
            position = last_sentence.find(oldSubclause)
            if position != -1:
                # If the subclause is found in the original sentence, replace it with the new active subclause
                modified_last_sentence = (
                    last_sentence[:position]
                    + newSubclause
                    + last_sentence[position + len(oldSubclause) :]
                )
                print("modified last sentence: ")
                print(modified_last_sentence)
                last_sentence = modified_last_sentence
            final_sentence = last_sentence

        final_sentence = final_sentence + ". "

        print(f"Passive Sentence: {doc}")
        print(f"Active Sentence: {final_sentence}")
        print("\n")
    except Exception as e:
        print(
            f"The following error accured during the final composition of the active sentence: {e}"
        )
        raise

    return final_sentence, activeSubclauses
