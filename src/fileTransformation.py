from pathlib import Path
import pandas as pd
import passiveToActive as pta
import spacy
import evaluation.evaluation as ev


nlp = spacy.load("en_core_web_lg")

source = "fileTransformation"
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

"""# Base directory as Path object (e.g. the directory of the script)
base_dir = Path(__file__).parent
parent_dir = base_dir.parent


# Input file and output file, which can be adapted as required
input_file_name = "goldstandard_rafi_v3.xlsx"
output_file_name = "Rafi_v3_Evaluation.xlsx"

# Create paths relative to the base directory
input_file = parent_dir / "data" / input_file_name
output_file = parent_dir / "data" / "tests" / output_file_name"""

# Ask the user for the input file path
input_file_path = input(
    "Please enter a valid path to the input file including the file name and extension (e.g., /path/to/InputFile.xlsx):\n "
)
output_file_path = input(
    "Please enter a valid path where the output file should be generated and saved including the file name and extension (e.g., /path/to/OutputFile.xlsx):\n "
)

# Convert the input paths to Path objects
input_file = Path(input_file_path)
output_file = Path(output_file_path)


try:
    # Load the Excel input file with the sentences to be transformed
    df = pd.read_excel(input_file)

    # Check if the input file has a column named "InputSentence"
    if "InputSentence" not in df.columns:
        raise ValueError("File needs to have a column named 'InputSentence'.")

    # Convert the sentences and save the output in a new column called "TransformedActiveSentence"

    df["TransformedActiveSentence"], df["TransformedSubclauses"] = zip(
        *df["InputSentence"].apply(
            lambda s: pta.passiveToActive(s, source) if isinstance(s, str) else (s, "-")
        )
    )
    # replace empty strings with a default value
    df["TransformedSubclauses"] = df["TransformedSubclauses"].apply(
        lambda x: {"000": "-"} if x is None or x == "" else x
    )

    def calculate_similarity(row):
        """
        This function takes a goldstandard sentence and the transformed active constructions as input, calculates the cosine semantic similarity with SBERT
        and returns the similarity score between the transformed construction and the corresponding part of the goldstandard sentence.
        """
        semantic_similarity = 0
        goldstandard = row["ReferenceSentence"]
        transformed = row["TransformedActiveSentence"]
        transformedSubclauses = row["TransformedSubclauses"]

        print(f"transformedSubclauses: {transformedSubclauses}")
        print(f"transformed: {transformed}")
        print(f"goldstandard: {goldstandard}")

        for subclause in transformedSubclauses.items():
            print(f"subclause: {subclause}")
            if "000" in subclause:
                final_semantic_similarity = None
                continue

            semantic_similarity += ev.evaluate_sentence_results(
                goldstandard, transformed, subclause, source
            )
            print(f"Individual Semantic Similarity:{semantic_similarity}")

            final_semantic_similarity = (
                semantic_similarity / len(transformedSubclauses)
                if transformedSubclauses
                else None
            )
        print(f"Semantic Similarity: {final_semantic_similarity}")
        return final_semantic_similarity

    # Calculate the semantic similarity score for each sentence with BERT
    def calculate_metrics(row):
        """
        Based on the calculated semantic similarities this function calculates the metrics like TP, FP, TN, FN to evaluate the output with precision and recall.

        If the similarity score is higher than 0.999, the sentence is correctly transformed and the function returns 1
        If the similarity score is lower than 0.999, the sentence is incorrectly transformed and the function returns 0

        Output: the calculated metrics
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
                "No passive construction identified" in row["TransformedActiveSentence"]
            ) and (row["Mode"] == "active"):
                TrueNegatives += 1  # correctly identified as active -> True Negatives
                return None
            elif (
                "No passive construction identified" in row["TransformedActiveSentence"]
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

            final_semantic_similarity = row["SemanticSimilarity"]
            if final_semantic_similarity is not None:
                if final_semantic_similarity > 0.95:
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

    # Ask user if s/he wants to evaluate the results
    evaluation = input("\n\nEvaluate Results? (y/n)\n\n")

    # Check if the input file has a column named "ReferenceSentence", otherwise evaluation is not possible
    if "ReferenceSentence" not in df.columns:
        raise ValueError("File needs to have a column named 'ReferenceSentence'.")

    if evaluation == "y":
        df["SemanticSimilarity"] = df.apply(calculate_similarity, axis=1)
        df.apply(calculate_metrics, axis=1)

    print("Spalten:")
    print(df.columns)

    # Order of the columns in the output file
    new_column_order = [
        "InputSentence",
        "TransformedActiveSentence",
    ] + [
        col for col in df.columns if col in ["ReferenceSentence", "SemanticSimilarity"]
    ]

    df = df[new_column_order]

    df.to_excel(output_file, index=False)

    FalseNegatives = FalseNegativesWronglyIdentified + FalseNegativesWronglyTransformed

    print("Transformation done.")
    if evaluation == "y":
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

        if (TruePositives + FalsePositives) != 0 and (
            TruePositives + FalseNegatives
        ) != 0:
            recall = TruePositives / (TruePositives + FalseNegatives)
            print(f"Recall: {recall}")
            precision = TruePositives / (TruePositives + FalsePositives)
            print(f"Precision: {precision}")
            f1_score = 2 * ((precision * recall) / (precision + recall))
            print(f"F1-Score: {f1_score}")

except Exception as e:
    print(f"An unexpected error occured during the evaluation of the ouput: {e}")
    raise
