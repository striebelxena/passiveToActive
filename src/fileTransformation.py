from pathlib import Path
import pandas as pd
import passiveToActive as pta
import spacy

nlp = spacy.load('en_core_web_lg')

# Basisverzeichnis als Path-Objekt (z.B. das Verzeichnis des Skripts)
base_dir = Path(__file__).parent
parent_dir = base_dir.parent

source = 'fileTransformation'

# Pfade relativ zum Basisverzeichnis bilden
input_file = parent_dir / 'data' / 'Goldstandard_XenaStriebel_V2.xlsx'
output_file = parent_dir / 'data' / 'Evaluation2.xlsx'

# Laden der Excel-Datei
df = pd.read_excel(input_file)

if 'PassiveSentence' not in df.columns:
    raise ValueError("File needs to have a column named 'PassiveSentence'.")

# Umwandeln der Sätze und Speichern in einer neuen Spalte
df['TransformedActiveSentence'] = df['PassiveSentence'].apply(lambda s: pta.passiveToActive(s, source) if isinstance(s, str) else s)
def calculate_similarity(row):
    goldstandard = nlp(row['ActiveSentence'])
    transformed = nlp(row['TransformedActiveSentence'])
    return goldstandard.similarity(transformed)

df['Similarity'] = df.apply(calculate_similarity, axis=1)

# Speichern der Ergebnisse in eine neue Excel-Datei
df.to_excel(output_file, index=False)

print("Transformation done.")
