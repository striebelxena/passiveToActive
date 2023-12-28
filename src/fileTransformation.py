from pathlib import Path
import pandas as pd
import passiveToActive

# Basisverzeichnis als Path-Objekt (z.B. das Verzeichnis des Skripts)
base_dir = Path(__file__).parent

# Pfade relativ zum Basisverzeichnis bilden
input_file = base_dir / 'data' / 'Goldstandard_XenaStriebel_V2.xlsx'
output_file = base_dir / 'data' / 'Evaluation.xlsx'

# Laden der Excel-Datei
df = pd.read_excel(input_file)

if 'PassiveSentence' not in df.columns:
    raise ValueError("File needs to have a column named 'PassiveSentence'.")

# Umwandeln der Sätze und Speichern in einer neuen Spalte
df['TransformedActiveSentence'] = df['PassiveSentence'].apply(lambda s: passiveToActive(s) if isinstance(s, str) else s)

# Speichern der Ergebnisse in eine neue Excel-Datei
df.to_excel(output_file, index=False)

print("Transformation done.")
