from pathlib import Path
import pandas as pd
import evaluation.fileEvaluation as ev

import passiveToActive as pta
import spacy
from bert_score import score


nlp = spacy.load("en_core_web_lg")

TrueNegatives = 0
TruePositives = 0
FalsePositives = 0
FalseNegatives = 0
CorrectlyIdentifiedAsPassive = 0
FalseNegativesWronglyIdentified = 0
FalseNegativesWronglyTransformed = 0

numbOfActiveSentences = 0
semanticSimilarity = 0

# Basisverzeichnis als Path-Objekt (z.B. das Verzeichnis des Skripts)
base_dir = Path(__file__).parent
parent_dir = base_dir.parent

source = "fileTransformation"
input_file_name = "Goldstandard_XenaStriebel_extended_with_ActiveSentences.xlsx"
output_file_name = "TestEvaluation2.xlsx"

# Pfade relativ zum Basisverzeichnis bilden
input_file = parent_dir / "data" / input_file_name
output_file = parent_dir / "data" / "tests" / output_file_name

# Laden der Excel-Datei
df = pd.read_excel(input_file)

if "PassiveSentence" not in df.columns:
    raise ValueError("File needs to have a column named 'PassiveSentence'.")

# Umwandeln der Sätze und Speichern in einer neuen Spalte
df["TransformedActiveSentence"] = df["PassiveSentence"].apply(
    lambda s: pta.passiveToActive(s, source) if isinstance(s, str) else s
)

print("Spalten:")
print(df.columns)

new_column_order = [
    "PassiveSentence",
    "ActiveSentence",
    "TransformedActiveSentence",
] + [
    col
    for col in df.columns
    if col not in ["PassiveSentence", "ActiveSentence", "TransformedActiveSentence"]
]

# Neuanordnung der Spalten im DataFrame
df = df[new_column_order]


def calculate_similarity(row):
    global Transformed
    global NotTransformed
    global TruePositives
    global FalsePositives
    global TrueNegatives
    global FalseNegatives
    global semanticSimilarity
    global CorrectlyIdentifiedAsPassive
    global FalseNegativesWronglyIdentified
    global FalseNegativesWronglyTransformed
    global numbOfActiveSentences

    if (row["TransformedActiveSentence"] == "No passive construction identified") and (
        row["Mode"] == "active"
    ):
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

    # goldstandard = nlp(row['ActiveSentence'])
    # transformed = nlp(row['TransformedActiveSentence'])
    goldstandard = row["ActiveSentence"]
    transformed = row["TransformedActiveSentence"]

    # semanticSimilarity= goldstandard.similarity(transformed)
    # goldstandard_bert = [goldstandard]
    # transformed_bert = [transformed]

    """print("Goldstandard_bert:")
    print(goldstandard)
    print("Output_bert:" )
    print( transformed)"""

    P, R, F1 = score(
        [transformed], [goldstandard], lang="en", model_type="bert-base-uncased"
    )
    print(f"BERT: Precision: {P.mean()}, Recall: {R.mean()}, F1-Score: {F1.mean()}")
    semanticSimilarity = F1
    if semanticSimilarity > 0.999:
        TruePositives += 1  # correctly transformed -> True Positives
    else:
        FalseNegativesWronglyTransformed += 1  # wrongly transformed -> False Negatives
    return semanticSimilarity


df["Semantic Similarity"] = df.apply(calculate_similarity, axis=1)


# Speichern der Ergebnisse in eine neue Excel-Datei

numOfPassiveSentences = (df["Mode"] == "passive").sum()
numbOfActiveSentences = (df["Mode"] == "active").sum()

# ev.evaluate_file_results(input_file_name, output_file_name)
df.to_excel(output_file, index=False)


print("Transformation done.")
print(f"Number of sentences transformed: {CorrectlyIdentifiedAsPassive+FalsePositives}")
print(f"TrueNegatives: {TrueNegatives}")
print(f"TruePositives: {TruePositives}")
print(f"FalsePositives: {FalsePositives}")
print(f"FalseNegativesWronglyIdentified: {FalseNegativesWronglyIdentified}")
print(f"FalseNegativesWronglyTransformed: {FalseNegativesWronglyTransformed}")
print(f"Number of sentences correctly transformed: {TruePositives}")
print(f"Number of sentences incorrectly transformed: {FalseNegatives}")

evaluation = input("\n\nEvaluate Results? (y/n)\n\n")

if evaluation == "y":
    FalseNegatives = FalseNegativesWronglyIdentified + FalseNegativesWronglyTransformed
    recall = TruePositives / (TruePositives + FalseNegatives)
    print(f"Recall: {recall}")
    precision = TruePositives / (TruePositives + FalsePositives)
    print(f"Precision: {precision}")
    # ev.evaluate_file_results(input_file_name, output_file_name)
