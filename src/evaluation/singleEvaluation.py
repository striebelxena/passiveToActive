
import spacy
import pandas as pd


# Evaluation
nlp = spacy.load('en_core_web_lg')

def evaluate_sentence_results (goldstandard, transformed):
    print("Goldstandard:" + goldstandard)
    print("Output:" + transformed)

    goldstandard = nlp(goldstandard)
    transformed = nlp(transformed)
    semantic_similarity = goldstandard.similarity(transformed)
    
        
    def get_dependency_types(doc):
        return [(token.head.i, token.i, token.dep_) for token in doc]

    deps1 = get_dependency_types(goldstandard)
    print(f"Dependencies 1: {deps1}")
    deps2 = get_dependency_types(transformed)
    print(f"Dependencies 2: {deps2}")

    similarities = sum(1 for dep1 in deps1 if dep1 in deps2) 
    print(f"Similarities: {similarities}")
    total_relations = max(len(deps1), len(deps2))
    print(f"Total relations: {total_relations}")
    dependency_similarity = similarities / total_relations
    
    print(f"Semantic Similarity: {semantic_similarity}")
    print(f"Dependency Similarity: {dependency_similarity}")
    
    

# Transform the sentences into Doc objects
"""sent1 = nlp("One ensures that and .  ")
sent2 = nlp("The sponsor and the investigator shall ensure that one conducts the clinical investigation in accordance with the approved clinical investigation plan. ")

similarity_1_2 = sent1.similarity(sent2)


print(f"Similarity between sentence 1 and 2: {similarity_1_2}")"""

