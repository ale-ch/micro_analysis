import polars as pl
import pandas as pd
import re
import os

cols = [
    'Ragione socialeCaratteri latini', 'Inactive', 'Quoted', 'Branch',
    'OwnData', 'Woco', 'Città Latin Alphabet', 'Codice ISO paese',
    'Codice NACE Rev. 2, core code (4 cifre)', 'Codice di consolidamento',
    'NUTS1', 'NUTS2', 'NUTS3', 'Latitudine', 'Longitudine',
    'Indirizzo/i aggiuntivo/i - Latitudine',
    'Indirizzo/i aggiuntivo/i - Longitudine',
    "Descrizione dell'attività (in inglese)", 'year',
    'Totale valore della produzione migl USD ', 'Numero dipendenti ',
    'Fatturato lordo migl USD ', 'Fatturato netto migl USD '
]

# Manual translations to English
translations = {
    'Ragione socialeCaratteri latini': 'Company name',
    'Città Latin Alphabet': 'City Latin alphabet',
    'Codice ISO paese': 'ISO country code',
    'Codice NACE Rev. 2, core code (4 cifre)': 'NACE Rev2 core code',
    'Codice di consolidamento': 'Consolidation code',
    'Latitudine': 'Latitude',
    'Longitudine': 'Longitude',
    'Indirizzo/i aggiuntivo/i - Latitudine': 'Additional address latitude',
    'Indirizzo/i aggiuntivo/i - Longitudine': 'Additional address longitude',
    "Descrizione dell'attività (in inglese)": 'Activity description en',
    'Totale valore della produzione migl USD ': 'Total production usd',
    'Numero dipendenti ': 'Number of employees',
    'Fatturato lordo migl USD ': 'Gross revenue usd',
    'Fatturato netto migl USD ': 'Net revenue usd'
}

translated = [translations.get(c, c) for c in cols]

def clean_names(columns):
    return (
        pd.Series(columns)
        .str.strip()
        .str.lower()
        .str.replace(r"'", "", regex=True)
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
        .tolist()
    )

cleaned_names = clean_names(translated)
print(cleaned_names)


directory = "/Volumes/T7 Shield/Downloads/panel_data"

files = [f for f in os.listdir(directory) if f.endswith(".csv") and not f.startswith(".")]

files = [os.path.join(directory, file) for file in files]

for file in files:
    output_file = os.path.join(directory, f"clean_{os.path.basename(file)}")
    df = pd.read_csv(file)

    df.columns = cleaned_names

    print(df.columns)

    df = df.replace("n.d.", "")

    print(f"Exporting {output_file}")
    df.to_csv(output_file, index=False)


# print(df.iloc[90:120,:])
