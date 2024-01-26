import spacy
import pattern_patch
import checkForPassive.passiveCheck as passiveCheck
import src.archive.sentenceParserOld as analyseSentence
import src.analysePassiveConstruction.sentenceParser as analyseSentenceTest

import verbConjugation.verbConjugator as verbConjugator
import src.composition.sentenceComposition as sentencComposition

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
        transformedSentence = sentencComposition.transformSentence(
            analysis_results, verbActive, preClause, postClause
        )

    print(f"Passive Sentence: {doc}")
    print(f"Active Sentence: {transformedSentence}")
    print("\n")

    return transformedSentence
