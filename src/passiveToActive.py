import spacy
import pattern_patch 
import checkForPassive.passiveCheck as passiveCheck
import parsingPOSTagging.sentenceParser as analyseSentence
import verbConjugation.verbConjugator as verbConjugator
import transformation.transformer as transformer

# Load NLP model
nlp = spacy.load("en_core_web_lg")


def passiveToActive(sentence):

    doc = nlp(sentence)
    pipeDoc = list(nlp.pipe(sentence))
    makedoc = nlp.make_doc(sentence)
    print("doc")
    print(doc)
    print("pipeDoc")
    print(pipeDoc)
    print("makedoc")
    print(makedoc)
    print("cats")
    print(doc.cats)
    print(nlp.pipe_names)
    # check if the sentence is passive
    isPassive = passiveCheck.checkForPassive(doc)
    if (isPassive != True):
        print("Sentence is not passive")
        exit()
    else: # if the sentence is passive, analyse the dependency, conjugate the verb and transform the sentence
        analysis_results = analyseSentence.analyseSentence(doc)
        print(f"results: {analysis_results}")
        verbActive = verbConjugator.conjugateVerb(analysis_results)
        transformedSentence = transformer.transformSentence(analysis_results, verbActive)

    print(f"Passive Sentence: {doc}")
    print(f"Active Sentence: {transformedSentence}")
    print('\n')