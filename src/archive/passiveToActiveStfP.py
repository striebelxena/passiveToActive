import os
from nltk.parse.stanford import StanfordParser


import spacy
import pattern_patch
import checkForPassive.passiveCheck as passiveCheck
import src.archive.sentenceParserOld as analyseSentence
import verbConjugation.verbConjugator as verbConjugator
import transformation.transformer as transformer


# Pfad zum Stanford Parser
stanford_parser_dir = "C:\\Users\\xstri\\OneDrive\\Master\\SemesterZwei\\NLPPraktikum\\PassiveToActiveWithNLP\\stanford-parser-full-2020-11-17"

os.environ["STANFORD_PARSER"] = stanford_parser_dir
os.environ["STANFORD_MODELS"] = stanford_parser_dir + "models"


parser = StanfordParser(
    model_path="C:\\Users\\xstri\\OneDrive\\Master\\SemesterZwei\\NLPPraktikum\\PassiveToActiveWithNLP\\stanford-corenlp-4.2.0.models-english.jar"
)
sentences = parser.raw_parse_sents(("Hello, this is a test.", "How are you?"))
for line in sentences:
    for sentence in line:
        sentence.draw()


"""
# Load NLP model
nlp = spacy.load("en_core_web_lg")


def passiveToActive(sentence, source):

    doc = nlp(sentence)
    
    
 

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
    """
