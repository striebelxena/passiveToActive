
import spacy

# Evaluation
nlp = spacy.load('en_core_web_lg')

# Transform the sentences into Doc objects
sent1 = nlp("One ensures that and .  ")
sent2 = nlp("The sponsor and the investigator shall ensure that one conducts the clinical investigation in accordance with the approved clinical investigation plan. ")

similarity_1_2 = sent1.similarity(sent2)


print(f"Similarity between sentence 1 and 2: {similarity_1_2}")

