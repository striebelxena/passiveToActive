import spacy
import checkForPassive.passiveCheck as passiveCheck
import parsingPOSTagging.sentenceParser as analyseSentence
import verbConjugation.verbConjugator as verbConjugator
import transformation.transformer as transformer

# Load NLP model
nlp = spacy.load("en_core_web_lg")

# Example sentence
# sentence = "Federal laws shall be adopted by the Bundestag."
sentence=input('\n\nPassive sentence:\n\n')

doc = nlp(sentence)

# check if the sentence is passive
isPassive = passiveCheck.checkForPassive(doc)
if (isPassive != True):
    print("Sentence is not passive")
    exit()
else: # if the sentence is passive, analyse the dependency, conjugate the verb and transform the sentence
   analysis_results = analyseSentence.analyseSentence(doc)
   print(f"results: {analysis_results}")
   verbActive = verbConjugator.conjugateVerb(analysis_results.get('verbLemma'), analysis_results.get('verbTense'), analysis_results.get('aNumber'))
   transformedSentence = transformer.transformSentence(doc, verbActive)

print(f"Passive Sentence: {doc}")
print('\n')