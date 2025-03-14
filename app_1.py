import pandas as pd
import streamlit as st
import sys
import os

# Stelle sicher, dass der Modulpfad korrekt hinzugefügt wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Projektarbeiten", "Streamlit", "datavis_g5")))

from analysis_1 import top_10_apps                                                                            # Import ohne Pfad-Probleme

# Datei laden und bereinigen
file_path = "googleplaystore_export.csv"

def load_data():
    return pd.read_csv(file_path)

df = load_data()

# Streamlit UI
st.title("Google Play Store Analyse")
option = st.selectbox("Wähle eine Analyse", ["Top 10 Apps Anzahl der Bewertungen"])

if option == "Top 10 Apps Anzahl der Bewertungen":
    top_10_apps(df)

st.success("Analyse erfolgreich durchgeführt.")
