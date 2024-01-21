from pathlib import Path
import pandas as pd
import evaluation.fileEvaluation as ev
import passiveToActive as pta
import spacy
from bert_score import score


nlp = spacy.load("en_core_web_lg")

# Metrics for the evaluation
TrueNegatives = 0
TruePositives = 0
FalsePositives = 0
FalseNegatives = 0
CorrectlyIdentifiedAsPassive = 0
FalseNegativesWronglyIdentified = 0
FalseNegativesWronglyTransformed = 0
numbOfActiveSentences = 0
semanticSimilarity = 0

# Base directory as Path object (e.g. the directory of the script)
base_dir = Path(__file__).parent
parent_dir = base_dir.parent

# Input file and output file
source = "fileTransformation"
input_file_name = "Goldstandard_XenaStriebel_extended_with_ActiveSentences.xlsx"
output_file_name = "TestEvaluation2.xlsx"

# Create paths relative to the base directory
input_file = parent_dir / "data" / input_file_name
output_file = parent_dir / "data" / "tests" / output_file_name

try:
    # Load the Excel input file
    df = pd.read_excel(input_file)

    # Check if the input file has a column named "PassiveSentence"
    if "PassiveSentence" not in df.columns:
        raise ValueError("File needs to have a column named 'PassiveSentence'.")

    # Convert the sentences and save the output in a new column called "TransformedActiveSentence"
    df["TransformedActiveSentence"] = df["PassiveSentence"].apply(
        lambda s: pta.passiveToActive(s, source) if isinstance(s, str) else s
    )

    print("Spalten:")
    print(df.columns)

    # Order of the columns in the output file
    new_column_order = [
        "PassiveSentence",
        "ActiveSentence",
        "TransformedActiveSentence",
    ] + [
        col
        for col in df.columns
        if col not in ["PassiveSentence", "ActiveSentence", "TransformedActiveSentence"]
    ]

    df = df[new_column_order]

    # Calcualte the semantic similarity score for each sentence with BERT
    def calculate_similarity(row):
        """
        This function takes a goldstandard sentence and the transformed sentence as input and returns the similarity score.
        Input: the output of the transformation function and the goldstandard sentence
        Steps:
        1. Calculate the semantic similarity score between output and goldstandard with BERT
        2. If the similarity score is higher than 0.999, the sentence is correctly transformed and the function returns 1
        3. If the similarity score is lower than 0.999, the sentence is incorrectly transformed and the function returns 0
        Output: the similarity score
        """

        global Transformed
        global NotTransformed
        global TruePositives  # correctly transformed -> True Positives
        global FalsePositives  # wrongly identified as passive -> False Positive
        global TrueNegatives  # correctly identified as active -> True Negatives
        global FalseNegatives  # wrongly identified as passive or wrongly transformed -> False Negatives
        global semanticSimilarity
        global CorrectlyIdentifiedAsPassive
        global FalseNegativesWronglyIdentified  # wrongly not identified as passive -> False Negatives
        global FalseNegativesWronglyTransformed  # wrongly transformed -> False Negatives
        global numbOfActiveSentences

        try:
            if (
                row["TransformedActiveSentence"] == "No passive construction identified"
            ) and (row["Mode"] == "active"):
                TrueNegatives += 1  # correctly identified as active -> True Negatives
                return None
            elif (
                row["TransformedActiveSentence"] == "No passive construction identified"
            ) and (row["Mode"] == "passive"):
                FalseNegativesWronglyIdentified += (
                    1  # wrongly not identified as passive -> False Negatives
                )
            elif (
                row["TransformedActiveSentence"] != "No passive construction identified"
            ) and (row["Mode"] == "passive"):
                CorrectlyIdentifiedAsPassive += 1  # correctly identified as passive
            elif (
                row["TransformedActiveSentence"] != "No passive construction identified"
            ) and (row["Mode"] == "active"):
                FalsePositives += 1  # wrongly identified as passive -> False Positive

            goldstandard = row["ActiveSentence"]
            transformed = row["TransformedActiveSentence"]

            # Calculate the semantic similarity score between output and goldstandard with BERT
            P, R, F1 = score(
                [transformed], [goldstandard], lang="en", model_type="bert-base-uncased"
            )
            print(
                f"BERT: Precision: {P.mean()}, Recall: {R.mean()}, F1-Score: {F1.mean()}"
            )
            semanticSimilarity = F1
            if semanticSimilarity > 0.999:
                TruePositives += 1  # correctly transformed -> True Positives
            else:
                FalseNegativesWronglyTransformed += (
                    1  # wrongly transformed -> False Negatives
                )
        except Exception as e:
            print(
                f"An unexpected error occured during the evaluation of the ouput: {e}"
            )
            raise

        return semanticSimilarity

    # Calculate the semantic similarity score for each sentence with BERT
    df["Semantic Similarity"] = df.apply(calculate_similarity, axis=1)

    # Store the semantic similarity score in a new column
    df.to_excel(output_file, index=False)

    # numOfPassiveSentences = (df["Mode"] == "passive").sum()
    # numbOfActiveSentences = (df["Mode"] == "active").sum()

    # ev.evaluate_file_results(input_file_name, output_file_name)

    print("Transformation done.")
    print(
        f"Number of sentences transformed: {CorrectlyIdentifiedAsPassive+FalsePositives}"
    )
    print(f"TrueNegatives: {TrueNegatives}")
    print(f"TruePositives: {TruePositives}")
    print(f"FalsePositives: {FalsePositives}")
    print(f"FalseNegativesWronglyIdentified: {FalseNegativesWronglyIdentified}")
    print(f"FalseNegativesWronglyTransformed: {FalseNegativesWronglyTransformed}")
    print(f"Number of sentences correctly transformed: {TruePositives}")
    print(f"Number of sentences incorrectly transformed: {FalseNegatives}")

    # Ask user if s/he wants to evaluate the results
    evaluation = input("\n\nEvaluate Results? (y/n)\n\n")

    if evaluation == "y":
        FalseNegatives = (
            FalseNegativesWronglyIdentified + FalseNegativesWronglyTransformed
        )
        recall = TruePositives / (TruePositives + FalseNegatives)
        print(f"Recall: {recall}")
        precision = TruePositives / (TruePositives + FalsePositives)
        print(f"Precision: {precision}")
        f1_score = 2 * ((precision * recall) / (precision + recall))
        print(f"F1-Score: {f1_score}")

        # ev.evaluate_file_results(input_file_name, output_file_name)
except Exception as e:
    print(f"An unexpected error occured during the evaluation of the ouput: {e}")
    raise
