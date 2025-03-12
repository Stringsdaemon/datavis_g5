import pandas as pd
import streamlit as st
import sys
import os

# Stelle sicher, dass der Modulpfad korrekt hinzugefügt wird
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Projektarbeiten", "Streamlit", "datavis_g5", "test_3")))

from analysis_3 import top_10_apps  # Import ohne Pfad-Probleme

# Datei laden und bereinigen
file_path = "google_clean_v2.csv"

def load_data():
    return pd.read_csv(file_path)

df = load_data()

# Streamlit UI
st.title("Google Play Store Analyse")

# Kategorien-Auswahl
categories = ["Alle Kategorien"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.selectbox("Wähle eine Kategorie", categories, key="category_select")

# Auswahl für Analyse
option = st.selectbox("Wähle eine Analyse", ["Top 10 Apps Anzahl der Bewertungen"])

if option == "Top 10 Apps Anzahl der Bewertungen":
    top_10_apps(df, selected_category)

# st.success("Analyse erfolgreich durchgeführt.")