import spacy
import pattern_patch 
from spacy.tokens import Token
import checkForPassive.passiveCheck as passiveCheck
import parsingPOSTagging.sentenceParser as analyseSentence
import verbConjugation.verbConjugator as verbConjugator
import transformation.transformer as transformer

# Load NLP model
nlp = spacy.load("en_core_web_lg")


def passiveToActive(sentence, source):

    doc = nlp(sentence)
    if not Token.has_extension("sentPosition"):
        Token.set_extension("sentPosition", default= 1)

    for token in doc:
        token._.sentPosition = token.i
    
 

    # check if the sentence is passive
    isPassive = passiveCheck.checkForPassive(doc)
    if (isPassive != True):
        print("Sentence is not passive")
        exit()
    else: # if the sentence is passive, analyse the dependency, conjugate the verb and transform the sentence
        analysis_results = analyseSentence.analyseSentence(doc, source)
        print(f"results: {analysis_results}")
        verbActive = verbConjugator.conjugateVerb(analysis_results)
        transformedSentence = transformer.transformSentence(analysis_results, verbActive)

    print(f"Passive Sentence: {doc}")
    print(f"Active Sentence: {transformedSentence}")
    print('\n')

    return transformedSentence