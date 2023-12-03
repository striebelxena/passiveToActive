import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Example sentence
sentence = "Federal laws shall be adopted by the Bundestag."

# Process the sentence
doc = nlp(sentence)

# POS Tagging
for token in doc:
    print(f"Word: {token.text}, POS Tag: {token.pos_}")

# Dependency Parsing
for token in doc:
    print(f"Word: {token.text}, Dependency: {token.dep_}, Head: {token.head.text}")

# Named Entity Recognition
for ent in doc.ents:
    print(f"Entity: {ent.text}, Label: {ent.label_}")

# Path: src/requirements.txt
# spacy==2.3.2
# en_core_web_sm==2.3.1
