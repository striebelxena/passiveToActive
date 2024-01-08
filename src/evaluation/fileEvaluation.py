
import spacy
from pathlib import Path
import pandas as pd


# Evaluation
nlp = spacy.load('en_core_web_lg')

#Basisverzeichnis als Path-Objekt (z.B. das Verzeichnis des Skripts)
base_dir = Path(__file__).parent.parent
parent_dir = base_dir.parent


#def evalute_sentence_results (sentence):


def evaluate_file_results (nameOfInputFile, nameOfOutputFile):
# Pfade relativ zum Basisverzeichnis bilden
    input_file = parent_dir / 'data' / nameOfInputFile
    output_file = parent_dir / 'data' / nameOfOutputFile

    # Laden der Excel-Datei
    df = pd.read_excel(input_file)

    def calculate_semantic_similarity(row):
        goldstandard = nlp(row['ActiveSentence'])
        transformed = nlp(row['TransformedActiveSentence'])
        semantic_similarity = goldstandard.similarity(transformed)
        return semantic_similarity
    
    def calculate_dependency_similarity (row):
        goldstandard = nlp(row['ActiveSentence'])
        transformed = nlp(row['TransformedActiveSentence'])
        print("Goldstandard:" + goldstandard)
        print("Output:" + transformed)
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
        similarity_score = similarities / total_relations
        print(f"Similarity score: {similarity_score}")

        return similarity_score
    

    df['Semantic Similarity'] = df.apply(calculate_semantic_similarity, axis=1)
    df['Dependency Similarity'] = df.apply(calculate_dependency_similarity, axis=1)
    df.to_excel(output_file, index=False)

    print("Semantic Similarity:" + df['Semantic Similarity'])
    print("Dependency Similarity:" + df['Dependency Similarity'])
    average_semantic_similarity = df['Semantic Similarity'].mean()
    average_dependency_similarity = df['Dependency Similarity'].mean()

    print("Durchschnittliche Semantic Similarity:", average_semantic_similarity)
    print("Durchschnittliche Dependency Similarity:", average_dependency_similarity)
    
    






# Transform the sentences into Doc objects
"""sent1 = nlp("One ensures that and .  ")
sent2 = nlp("The sponsor and the investigator shall ensure that one conducts the clinical investigation in accordance with the approved clinical investigation plan. ")

similarity_1_2 = sent1.similarity(sent2)


print(f"Similarity between sentence 1 and 2: {similarity_1_2}")"""

