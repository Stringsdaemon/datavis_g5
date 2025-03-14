import pandas as pd
import streamlit as st
import plotly.express as px
import time


def top_10_apps(df, category):
    """Erstellt ein interaktives und animiertes Diagramm der Top 10 Apps nach Bewertungen für eine ausgewählte Kategorie."""
    df = df.copy()
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype(int)

    # Filter nach Kategorie
    if category != "Alle Kategorien":
        df = df[df["Category"] == category]

    # Entferne doppelte Apps und nehme nur die höchsten Bewertungen pro App
    top_apps = df.sort_values(by="Reviews", ascending=False).drop_duplicates(subset=["App"]).head(10)
    top_apps = top_apps.sort_values(by="Reviews", ascending=True)  # Sortiere für Animation

    chart = st.empty()
    speed = st.slider("Animationsgeschwindigkeit", 0.05, 1.0, 0.2, 0.05)
    start_animation = st.button("▶️")

    if start_animation:
        y_max = max(1000000, top_apps["Reviews"].max() * 1.2)  # Dynamische Skalierung

        for i in range(1, 51):
            top_apps["Animated_Reviews"] = (top_apps["Reviews"] * i / 50).astype(int)
            fig = px.bar(top_apps, x="App", y="Animated_Reviews",
                         title=f"Top 10 Apps nach Anzahl der Bewertungen ({category})",
                         text=top_apps["Animated_Reviews"].apply(lambda x: f"{x:,}"))
            fig.update_traces(textposition="outside")
            fig.update_yaxes(range=[0, y_max])
            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(speed / 5)


# Streamlit UI für Kategorie-Auswahl
st.title("Google Play Store Analyse")

# Lade Daten
file_path = "google_clean_v2.csv"
df = pd.read_csv(file_path)

# Kategorien-Auswahl
categories = ["Alle Kategorien"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.selectbox("Wähle eine Kategorie", categories)

top_10_apps(df, selected_category)
