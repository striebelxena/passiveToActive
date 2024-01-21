import spacy
import pandas as pd
from bert_score import score

nlp = spacy.load("en_core_web_lg")


def evaluate_sentence_results(goldstandard, transformed):
    """
    This function takes a goldstandard sentence and the transformed sentence as input and returns the similarity score.
    Input: the output of the transformation function and the goldstandard sentence
    Steps:
    1. Calculate the semantic similarity score between output and goldstandard with BERT
    2. Calculate the dependency similarity score
    Output: the similarity score
    """

    goldstandard_bert = [goldstandard]
    transformed_bert = [transformed]

    print("Goldstandard_bert:")
    print(goldstandard_bert)
    print("Output_bert:")
    print(transformed_bert)

    try:
        # Calculate the semantic similarity score between output and goldstandard with BERT
        P, R, F1 = score(
            transformed_bert,
            goldstandard_bert,
            lang="en",
            model_type="bert-base-uncased",
        )
        print(f"BERT: Precision: {P.mean()}, Recall: {R.mean()}, F1-Score: {F1.mean()}")

        semantic_similarity = F1.mean()

        # Calculate the dependency similarity score
        def get_dependency_types(doc):
            return [(token.head.i, token.i, token.dep_) for token in doc]

        deps1 = get_dependency_types(goldstandard)
        deps2 = get_dependency_types(transformed)

        similarities = sum(1 for dep1 in deps1 if dep1 in deps2)
        print(f"Similarities: {similarities}")
        total_relations = max(len(deps1), len(deps2))
        print(f"Total relations: {total_relations}")
        dependency_similarity = similarities / total_relations
    except Exception as e:
        print(f"An unexpected error occured during the evaluation of the ouput: {e}")
        raise

    return semantic_similarity, dependency_similarity
