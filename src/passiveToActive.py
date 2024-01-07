import spacy
import pattern_patch 
import checkForPassive.passiveCheck as passiveCheck
import parsingPOSTagging.sentenceParser as analyseSentence
import parsingPOSTagging.sentenceParserTest as analyseSentenceTest

import verbConjugation.verbConjugator as verbConjugator
import transformation.transformer as transformer

# Load NLP model
nlp = spacy.load("en_core_web_lg")


def passiveToActive(sentence, source):

    activeSentences = {}


    doc = nlp(sentence)
    
    
        # check if the sentence is passive
    identifiedPassiveSentences, preClause, postClause, indicesOfSubtrees = passiveCheck.checkForPassive(doc)
    #identifiedPassiveSentence = str(identifiedPassiveSentence)
    if (identifiedPassiveSentences == False):
        print("Sentence is not passive")
        exit()
    else: # if the sentence is passive, analyse the dependency, conjugate the verb and transform the sentence
        for index, sentence in enumerate(identifiedPassiveSentences):      
            passiveSentence = nlp(sentence.text)
            analysis_results = analyseSentenceTest.analyseSentence(passiveSentence, source)
            print(f"results: {analysis_results}")
            verbActive = verbConjugator.conjugateVerb(analysis_results)
            transformedSentence = transformer.transformSentence(analysis_results, verbActive, preClause[index], postClause[index])
            activeSentences[f'{indicesOfSubtrees[index]}']= transformedSentence
            
            print(indicesOfSubtrees)
            print("Active Sentences: ")
            print(activeSentences)
            print(f"Active Subsentence: {transformedSentence}")
            print("-------------------------------------")


    def calc_diff(key):
        start, end = key.split(',')
        return int(end) - int(start)
    
    activeSentsSorted = dict(sorted(activeSentences.items(), key=lambda item: calc_diff(item[0])))
    print("Sorted Active Sentences: ")
    print(activeSentsSorted)

    #Combine the active sentences into one sentence using the indices
    indices_list = list(activeSentsSorted.keys())
    if len(indices_list) == 1: #if there is only one sentence, return it
        return transformedSentence
    last_indices = indices_list[-1]
    last_sentence = activeSentsSorted[last_indices].split()

    for indices in indices_list:
        if indices == last_indices:
            break
        current_indices= indices
        start_index, end_index = map(int, current_indices.split(','))
        current_sentence = activeSentsSorted[current_indices].split()
        
        text = current_sentence[start_index:end_index+1]
        print("current_indices")
        print(current_indices)
        print("text")
        print(text)
        if "not" in sentence:
            modified_last_sentence = " ".join(last_sentence[:start_index]) +" "+  " ".join(text) +" " + " ".join(last_sentence[end_index:])

        
        modified_last_sentence = " ".join(last_sentence[:start_index]) +" "+  " ".join(text) +" " + " ".join(last_sentence[end_index:])
        print("modified last sentence: ")
        print(modified_last_sentence)
        last_sentence = modified_last_sentence
        final_sentence = last_sentence


    print(f"Passive Sentence: {doc}")
    print(f"Active Sentence: {final_sentence}")
    print('\n')

    return final_sentence