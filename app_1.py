import pandas as pd
import streamlit as st
from analysis import top_10_apps

# Datei laden und bereinigen
file_path = "googleplaystore_export.csv"

def load_data():
    return pd.read_csv(file_path)

df = load_data()

# Streamlit UI
st.title("Google Play Store Analyse")
option = st.selectbox("Wähle eine Analyse", ["Top 10 Apps nach Bewertungen"])

if option == "Top 10 Apps nach Bewertungen":
    top_10_apps(df)

st.success("Analyse erfolgreich durchgeführt.")
