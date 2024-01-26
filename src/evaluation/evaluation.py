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
    # goldstandard_bert = [goldstandard]
    goldstandard = nlp(goldstandard)
    # transformed_bert = [transformedSentence]
    # transformedSubclause_bert = [transformedSubclause]
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
        if token.pos_ == "VERB" and (token.lemma_ == verbLemma):
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

    transformedSubclause = (
        transformedSubclause.text
        if isinstance(transformedSubclause, spacy.tokens.doc.Doc)
        else transformedSubclause
    )

    # if lenSubclauseGoldstandard > lenTransformedSubclause:
    # If no subclause has been identified, the whole sentences are compared instead of the subclauses
    if subclauseGoldstandard == None or len(subclauseGoldstandard) == 0:
        subclauseGoldstandard = goldstandard.text
        transformedSubclause = transformedSentence

    # SBERT
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Berechnen der Einbettungen (Embeddings)
    embedding1 = model.encode(transformedSubclause, convert_to_tensor=False)
    embedding2 = model.encode(subclauseGoldstandard, convert_to_tensor=False)

    # Berechnen der Ähnlichkeit
    SBERT_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    SBERT_similarity = SBERT_similarity.item()

    print("SBERT Score:", SBERT_similarity)

    return SBERT_similarity
