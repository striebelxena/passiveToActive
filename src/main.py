import spacy
import checkForPassive.passiveCheck as passiveCheck
import parsingPOSTagging.sentenceParser as analyseSentence
import verbConjugation.verbConjugator as verbConjugator
import transformation.transformer as transformer

# Load NLP model
nlp = spacy.load("en_core_web_md")

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
   analyseSentence.analyseSentence(doc)
   verbActive = verbConjugator.conjugateVerb(doc)
   transformedSentence = transformer.transformSentence(doc, verbActive)

print(f"Passive Sentence: {doc}")
print(f"Active Sentence: {transformedSentence}")
print('\n')