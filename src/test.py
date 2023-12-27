import spacy


nlp = spacy.blank("en")

sentence=input('\n\nPassive sentence:\n\n')
doc = nlp(sentence)

for word in doc:
    print(word.text)