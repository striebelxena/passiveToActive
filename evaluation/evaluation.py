
# Evaluation
transformed_doc = nlp(transformedSentence)
similarity_1_2 = doc.similarity(transformed_doc)

print(f"Similarity between sentence 1 and 2: {similarity_1_2}")

