import spacy
import pattern_patch
import checkForPassive.passiveCheck as passiveCheck
import parsingPOSTagging.sentenceParser as analyseSentence
import parsingPOSTagging.sentenceParserTest as analyseSentenceTest

import verbConjugation.verbConjugator as verbConjugator
import transformation.transformer as transformer
from langdetect import detect


# Load NLP model
nlp = spacy.load("en_core_web_lg")


def passiveToActive(sentence, source):
    activeSentences = {}
    oldSentences = {}
    newLengths = {}

    if detect(sentence) != "en":
        return "Sentence is not in English"

    sentence = sentence.strip()

    doc = nlp(sentence)

    # check if the sentence is passive
    (
        identifiedPassiveSentences,
        preClause,
        postClause,
        indicesOfSubtrees,
    ) = passiveCheck.checkForPassive(doc)
    # identifiedPassiveSentence = str(identifiedPassiveSentence)
    if identifiedPassiveSentences == False:
        return "No passive construction identified"
    else:  # if the sentence is passive, analyse the dependency, conjugate the verb and transform the sentence
        for index, sentence in enumerate(identifiedPassiveSentences):
            passiveSentence = nlp(sentence.text)
            analysis_results = analyseSentenceTest.analyseSentence(
                passiveSentence, source
            )
            print(f"results: {analysis_results}")
            verbActive = verbConjugator.conjugateVerb(analysis_results)
            transformedSentence, newLength = transformer.transformSentence(
                analysis_results, verbActive, preClause[index], postClause[index]
            )
            activeSentences[f"{indicesOfSubtrees[index]}"] = transformedSentence
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
            print("-------------------------------------")

    def calc_diff(key):
        start, end = key.split(",")
        return int(end) - int(start)

    activeSentsSorted = dict(
        sorted(activeSentences.items(), key=lambda item: calc_diff(item[0]))
    )
    print("Sorted Active Sentences: ")
    print(activeSentsSorted)

    # Combine the active sentences into one sentence using the indices
    indices_list = list(activeSentsSorted.keys())
    if len(indices_list) == 1:  # if there is only one sentence, return it
        transformedSentence = activeSentsSorted[indices_list[0]] + ". "
        print(f"Passive Sentence: {doc}")
        print(f"Active Sentence: {transformedSentence}")
        print("\n")
        return transformedSentence
    last_indices = indices_list[-1]
    last_sentence = " ".join(activeSentsSorted[last_indices].split())

    for current_indices in indices_list:
        if current_indices == last_indices:
            break

        start_index, end_index = map(int, current_indices.split(","))
        end_index = start_index + newLengths[current_indices]  # + 1
        current_sentence = " ".join(activeSentsSorted[current_indices].split())
        current_sentence = nlp(current_sentence)

        oldSubclause = oldSentences[current_indices]
        if oldSubclause.endswith("."):
            oldSubclause = oldSubclause[:-1]

        print("old subclause")
        print(oldSubclause)
        print("current sentence: ")
        print(activeSentsSorted[current_indices])
        """
        substring_index = None
        for i, word in enumerate(last_sentence):
            if word == oldSubclause:
                substring_index = i
                break
        print("substring index: ")
        print(substring_index)
        
        if substring_index is not None:
            newSubclause =current_sentence[start_index:end_index+1]
            modified_last_sentence = last_sentence[:substring_index] + newSubclause + last_sentence[substring_index+len(oldSubclause):]
            print("modified last sentence: ")
            print(modified_last_sentence)
        last_sentence = modified_last_sentence
        final_sentence = last_sentence

    final_sentence = final_sentence + "."


        #current_sentence = nlp(current_sentence)
"""
        newSubclause = current_sentence[start_index : end_index + 1]
        newSubclause = [token.text for token in newSubclause]
        newSubclause = " ".join(newSubclause).strip()

        print(current_sentence[start_index - 2])
        print(current_sentence[start_index - 1])
        print(current_sentence[start_index])

        print("current_indices")
        print("start_index: ", start_index)
        print("end_index: ", end_index)
        print(current_indices)
        print("new clause")
        print(newSubclause)

        position = last_sentence.find(oldSubclause)
        if position != -1:
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

    return final_sentence


"""
        if "not" in sentence:
            modified_last_sentence = " ".join(last_sentence[:start_index]) +" "+  " ".join(text) +" " + " ".join(last_sentence[end_index:])

        
        modified_last_sentence = " ".join(last_sentence[:start_index]) +" "+  " ".join(text) +" " + " ".join(last_sentence[end_index:])
        print("modified last sentence: ")
        print(modified_last_sentence)
        last_sentence = modified_last_sentence
        final_sentence = last_sentence
"""
