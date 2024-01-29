from pathlib import Path
import pandas as pd
import passiveToActive as pta
import spacy
import evaluation.evaluation as ev
from tqdm import tqdm
import questionary
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import time

console = Console()

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

try:
    # Ask the user for the input file path
    input_file_path = questionary.path(
        "\nPlease enter a valid path to the input file including the file name and extension (e.g., /path/to/InputFile.xlsx):\n "
    ).ask()
    output_file_path = questionary.path(
        "\nPlease enter a valid path where the output file should be generated and saved including the file name and extension (e.g., /path/to/OutputFile.xlsx):\n "
    ).ask()

    # Convert the input paths to Path objects
    input_file = Path(input_file_path)
    output_file = Path(output_file_path)
except Exception as e:
    console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
    raise

try:
    # Load the Excel input file with the sentences to be transformed
    df = pd.read_excel(input_file)

    # Check if the input file has a column named "InputSentence"
    if "InputSentence" not in df.columns:
        raise ValueError("File needs to have a column named 'InputSentence'.")

    # Convert the sentences and save the output in a new column called "TransformedActiveSentence"
    transformed_data = []
    for sentence in tqdm(
        df["InputSentence"], total=df.shape[0], desc="\nProcessing Sentences"
    ):
        if isinstance(sentence, str):
            result = pta.passiveToActive(sentence, source)
        else:
            result = (sentence, "-")
        transformed_data.append(result)

    df["TransformedActiveSentence"], df["TransformedSubclauses"] = zip(
        *transformed_data
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

        for subclause in transformedSubclauses.items():
            if "000" in subclause:
                final_semantic_similarity = None
                continue

            semantic_similarity += ev.evaluate_sentence_results(
                goldstandard, transformed, subclause, source
            )

            final_semantic_similarity = (
                semantic_similarity / len(transformedSubclauses)
                if transformedSubclauses
                else None
            )
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
    evaluation = questionary.confirm("\n\nEvaluate Results? (y/n)\n\n").ask()

    # Check if the input file has a column named "ReferenceSentence", otherwise evaluation is not possible
    if "ReferenceSentence" not in df.columns:
        raise ValueError("File needs to have a column named 'ReferenceSentence'.")

    if evaluation:
        # Using tqdm to show progress for the SemanticSimilarity calculation
        similarities = []
        for index, row in tqdm(
            df.iterrows(), total=df.shape[0], desc="Calculating Semantic Similarity"
        ):
            similarity = calculate_similarity(row)
            similarities.append(similarity)

        df["SemanticSimilarity"] = similarities
        df.apply(calculate_metrics, axis=1)

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
    if (TruePositives + FalsePositives) != 0 and (TruePositives + FalseNegatives) != 0:
        recall = TruePositives / (TruePositives + FalseNegatives)
        precision = TruePositives / (TruePositives + FalsePositives)
        f1_score = 2 * ((precision * recall) / (precision + recall))
    rprint("\n[bold green]Transformation done.[/bold green]")
    if evaluation:
        table = Table(show_header=True, header_style="bold white")
        table.add_column("Metric", style="dim")
        table.add_column("Value", justify="right")
        table.add_row(
            "Number of sentences transformed",
            str(CorrectlyIdentifiedAsPassive + FalsePositives),
        )
        table.add_row("True Negatives", str(TrueNegatives))
        table.add_row("True Positives", str(TruePositives))
        table.add_row("False Positives", str(FalsePositives))
        table.add_row("False Negatives", str(FalseNegatives))
        table.add_row(
            "False Negatives Wrongly Identified", str(FalseNegativesWronglyIdentified)
        )
        table.add_row(
            "False Negatives Wrongly Transformed", str(FalseNegativesWronglyTransformed)
        )
        table.add_row("Recall", str(recall))
        table.add_row("Precision", str(precision))

        table.add_row(
            "F1-Score",
            str(f1_score),
        )
        console.print(table)


except Exception as e:
    console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
    raise
