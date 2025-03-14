import streamlit as st
from analysis_bottom_apps import get_bottom_10_apps_by_rating
from analysis_top_genres import get_top_10_genres_by_installs
from visualization_6 import animate_chart, visualize_bottom_apps, visualize_top_genres

# Daten laden
def load_data():
    import pandas as pd
    return pd.read_csv("google_clean_v2.csv")

df = load_data()

# Auswahl der Analyse
st.title("📊 App-Analyse Dashboard")
analyse_option = st.selectbox("Wähle eine Analyse:", [
    "Top 10 Apps mit den meisten Bewertungen",
    "Top 10 Apps mit den schlechtesten Bewertungen",
    "Top 10 App-Genres nach Downloads"
])

if analyse_option == "Top 10 Apps mit den meisten Bewertungen":
    top_apps = df.nlargest(10, "Reviews")
    animate_chart(top_apps, "App", "Reviews", "📊 Top 10 Apps nach Anzahl der Bewertungen", "App")

elif analyse_option == "Top 10 Apps mit den schlechtesten Bewertungen":
    visualize_bottom_apps(df)

elif analyse_option == "Top 10 App-Genres nach Downloads":
    visualize_top_genres(df)
