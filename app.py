#%%
import pandas as pd
import streamlit as st

# Datei laden und bereinigen
file_path = "googleplaystore.csv"
output_file = "googleplaystore_export.csv"


def load_and_clean_data():
    try:
        df = pd.read_csv(file_path, encoding='utf-8')

        # Entferne doppelte App-Einträge, behalte nur die aktuellste Version
        df = df.sort_values(by=["App", "Last Updated"], ascending=[True, False])
        df = df.drop_duplicates(subset=["App"], keep="first")

        # Bereinige numerische Spalten
        df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

        # Bereinige die Installs-Spalte, entferne ungültige Werte
        df["Installs"] = df["Installs"].str.replace(r"[+,]", "", regex=True)
        df = df[df["Installs"].str.isnumeric()]  # Entfernt Zeilen mit nicht-numerischen Werten
        df["Installs"] = df["Installs"].astype(float)

        # Bereinige die Price-Spalte
        df["Price"] = df["Price"].str.replace("$", "", regex=True)
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

        # Standardisiere "Type"-Spalte
        df["Type"] = df["Type"].fillna("Free")

        # Entferne fehlerhafte oder fehlende Werte
        df = df.dropna()

        # Speichere die bereinigte Datei
        df.to_csv(output_file, index=False)

        return df
    except FileNotFoundError:
        st.error("Fehler: Datei nicht gefunden.")
        return pd.DataFrame()


df = load_and_clean_data()

# Streamlit UI
st.title("Google Play Store Analyse")
st.dataframe(df)

st.success(f"Bereinigte Datei wurde erfolgreich als {output_file} gespeichert.")
