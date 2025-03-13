import streamlit as st
from data_loader_6 import load_data
from analysis_top_apps_6 import get_top_10_apps
from analysis_content_rating_6 import get_content_rating_distribution

from visualization_animations_6 import animate_chart
from visualization_top_apps_6 import visualize_bottom_10_apps
from visualization_content_rating_6 import visualize_content_rating
from visualization_genres_6 import visualize_top_genres_by_installs

# Daten laden
df = load_data()

st.write("📊 Geladene Daten Vorschau:")
st.write(df.head())

# Streamlit UI
st.title("📊 Google Play Store Analyse")
st.markdown("Entdecken Sie die beliebtesten Apps nach Bewertungen")

# Kategorien-Auswahl
categories = ["Alle Kategorien"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.selectbox("📂 Wähle eine Kategorie", categories, key="category_select")

# Auswahl für Analyseoptionen
analysis_options = [
    "Top 10 Apps Anzahl der Bewertungen",
    "Top 10 Apps mit den schlechtesten Bewertungen",
    "Anzahl der Apps pro Inhaltsbewertung",
    "Beliebteste App-Genres basierend auf Downloads"
]
selected_analysis = st.selectbox("📈 Wähle eine Analyse", analysis_options)

# Diagrammauswahl
chart_types = ["Balkendiagramm", "Kreisdiagramm", "Liniendiagramm"]
selected_chart_type = st.selectbox("📊 Wähle einen Diagrammtyp", chart_types)

if selected_analysis == "Top 10 Apps Anzahl der Bewertungen":
    st.markdown(f"### 📱 Top 10 Apps in der Kategorie: **{selected_category}**")
    top_apps = get_top_10_apps(df)
    animate_chart(top_apps, selected_chart_type, selected_category)

elif selected_analysis == "Top 10 Apps mit den schlechtesten Bewertungen":
    st.markdown("### 📉 Top 10 Apps mit den schlechtesten Bewertungen")
    visualize_bottom_10_apps(df)

elif selected_analysis == "Anzahl der Apps pro Inhaltsbewertung":
    st.markdown("### 📊 Anzahl der Apps pro Inhaltsbewertung")
    visualize_content_rating(df)

elif selected_analysis == "Beliebteste App-Genres basierend auf Downloads":
    st.markdown("### 🎮 Beliebteste App-Genres basierend auf Downloads")
    visualize_top_genres_by_installs(df)