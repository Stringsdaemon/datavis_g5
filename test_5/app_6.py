import pandas as pd
import streamlit as st
import sys
import os

# Stelle sicher, dass der Modulpfad korrekt hinzugefügt wird
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "Projektarbeiten", "Streamlit", "datavis_g5", "test_4")))

from analysis_5 import get_top_10_apps
from visualization_5 import animate_chart

# Datei laden und bereinigen
def load_data():
    file_path = "google_clean_v2.csv"
    return pd.read_csv(file_path)

df = load_data()

# Streamlit UI
st.title("📊 Google Play Store Analyse")

# Kategorien-Auswahl ohne unnötige Überschrift
selected_category = st.selectbox("", ["Alle Kategorien"] + sorted(df["Category"].dropna().unique().tolist()), key="category_select")

# Lade die Top 10 Apps für die gewählte Kategorie
top_apps = get_top_10_apps(df, selected_category)

if not top_apps.empty:
    animate_chart(top_apps)
else:
    st.warning("⚠️ Keine Apps in dieser Kategorie gefunden.")
