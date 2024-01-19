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
    doc = nlp(sentence)

    # check if the sentence is passive
    identifiedPassiveSentence, preClause, postClause = passiveCheck.checkForPassive(doc)
    identifiedPassiveSentence = str(identifiedPassiveSentence)
    if identifiedPassiveSentence == False:
        exit()
    else:  # if the sentence is passive, analyse the dependency, conjugate the verb and transform the sentence
        passiveSentence = nlp(identifiedPassiveSentence)
        analysis_results = analyseSentenceTest.analyseSentence(passiveSentence, source)
        print(f"results: {analysis_results}")
        verbActive = verbConjugator.conjugateVerb(analysis_results)
        transformedSentence = transformer.transformSentence(
            analysis_results, verbActive, preClause, postClause
        )

    print(f"Passive Sentence: {doc}")
    print(f"Active Sentence: {transformedSentence}")
    print("\n")

    return transformedSentence
