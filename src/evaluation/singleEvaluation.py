import spacy
import pandas as pd
from bert_score import score
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_lg")


def evaluate_sentence_results(
    goldstandard, transformedSentence, transformedSubclause, source
):
    """
    This function takes a goldstandard sentence and the transformed sentence as input and returns the similarity score.
    Input: the output of the transformation function and the goldstandard sentence
    Steps:
    1. Calculate the semantic similarity score between output and goldstandard with BERT
    2. Calculate the dependency similarity score
    Output: the similarity score
    """
    print(f"finalTransformedSubclauses: {transformedSubclause}")
    goldstandard_bert = [goldstandard]
    goldstandard = nlp(goldstandard)
    transformed_bert = [transformedSentence]
    transformedSubclause_bert = [transformedSubclause]
    if source == "singleTransformation":
        transformedSubclause = nlp(transformedSubclause)
    else:
        transformedSubclause = nlp(transformedSubclause[1])
    print(f"transformedSubclause after nlp: {transformedSubclause}")
    subclauseGoldstandard = None

    for token in transformedSubclause:
        print(f"token: {token}")
        if token.dep_ == "ROOT":
            verbLemma = token.lemma_
            print(f"verbLemma transformed: {verbLemma}")
            break

    for token in goldstandard:
        if token.pos_ == "VERB" and (
            token.lemma_ == verbLemma
            or token.lemma_ == "fulfill"  # due to differences between BE and AE
        ):
            print("token lemma:  goldstandard")
            print(token.lemma_)
            subclauseGoldstandard = token.subtree
            subclauseGoldstandard = "".join(
                token.text + " "
                if token.text == ","
                else token.text_with_ws
                if not token.is_punct
                else token.text
                for token in subclauseGoldstandard
            )
            if subclauseGoldstandard.endswith(".") or subclauseGoldstandard.endswith(
                ". "
            ):
                subclauseGoldstandard = subclauseGoldstandard[:-1]
            break

    print(f"subclauseGoldstandard: {subclauseGoldstandard}")
    print(f"transformedSubclauses: {transformedSubclause}")

    # SBERT
    model = SentenceTransformer("all-MiniLM-L6-v2")
    if subclauseGoldstandard == None:
        subclauseGoldstandard = goldstandard.text

    transformedSubclause = (
        transformedSubclause.text
        if isinstance(transformedSubclause, spacy.tokens.doc.Doc)
        else transformedSubclause
    )
    # Berechnen der Einbettungen (Embeddings)
    embedding1 = model.encode(transformedSubclause, convert_to_tensor=False)
    embedding2 = model.encode(subclauseGoldstandard, convert_to_tensor=False)

    # Berechnen der Ähnlichkeit
    SBERT_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    SBERT_similarity = SBERT_similarity.item()

    print("SBERT Score:", SBERT_similarity)

    try:
        # Calculate the semantic similarity score between output and goldstandard with BERT/SBERT
        P, R, F1 = score(
            [transformedSubclause],
            [subclauseGoldstandard],
            lang="en",
            model_type="bert-base-uncased",
        )
        # print(f"BERT: Precision: {P.mean()}, Recall: {R.mean()}, F1-Score: {F1.mean()}")

        BERT_similarity = F1.mean()
        """
        # Calculate the dependency similarity score
        def get_dependency_types(doc):
            return [(token.head.i, token.i, token.dep_) for token in doc]

        deps1 = get_dependency_types(goldstandard)
        deps2 = get_dependency_types(transformedSentence)

        similarities = sum(1 for dep1 in deps1 if dep1 in deps2)
        print(f"Similarities: {similarities}")
        total_relations = max(len(deps1), len(deps2))
        print(f"Total relations: {total_relations}")
        dependency_similarity = similarities / total_relations"""
    except Exception as e:
        print(f"An unexpected error occured during the evaluation of the ouput: {e}")
        raise

    return SBERT_similarity
