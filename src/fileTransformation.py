from pathlib import Path
import pandas as pd
import evaluation.fileEvaluation as ev

import passiveToActive as pta
import spacy

nlp = spacy.load('en_core_web_lg')

countTransformed = 0 #Number of sentences that were identified as passive and transformed
countNotTransformed = 0 #Number of sentences that were not identified as passive and therefore not transformed

# Basisverzeichnis als Path-Objekt (z.B. das Verzeichnis des Skripts)
base_dir = Path(__file__).parent
parent_dir = base_dir.parent

source = 'fileTransformation'
input_file_name = 'goldstandard_rafi.xlsx'
output_file_name = 'TestEvaluationRafi.xlsx'

# Pfade relativ zum Basisverzeichnis bilden
input_file = parent_dir / 'data' / input_file_name
output_file = parent_dir / 'data' /'tests'/ output_file_name

# Laden der Excel-Datei
df = pd.read_excel(input_file)

if 'PassiveSentence' not in df.columns:
    raise ValueError("File needs to have a column named 'PassiveSentence'.")

# Umwandeln der Sätze und Speichern in einer neuen Spalte
df['TransformedActiveSentence'] = df['PassiveSentence'].apply(lambda s: pta.passiveToActive(s, source) if isinstance(s, str) else s)

print("Spalten:")
print(df.columns)

new_column_order = ['PassiveSentence', 'ActiveSentence','TransformedActiveSentence'] + [col for col in df.columns if col not in ['PassiveSentence', 'ActiveSentence','TransformedActiveSentence']]

# Neuanordnung der Spalten im DataFrame
df = df[new_column_order]


def calculate_similarity(row):
    global countTransformed  
    global countNotTransformed 
    if (row['TransformedActiveSentence'] == "Sentence already active"):
        countNotTransformed += 1
        return None
    else:
        countTransformed += 1
    goldstandard = nlp(row['ActiveSentence'])
    transformed = nlp(row['TransformedActiveSentence'])
    return goldstandard.similarity(transformed)

df['Semantic Similarity'] = df.apply(calculate_similarity, axis=1)




# Speichern der Ergebnisse in eine neue Excel-Datei
df.to_excel(output_file, index=False)


#ev.evaluate_file_results(input_file_name, output_file_name)


print("Transformation done.")
print(f"Number of sentences transformed: {countTransformed}")
print(f"Number of sentences not transformed: {countNotTransformed}")
