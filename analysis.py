import pandas as pd
import streamlit as st
import plotly.express as px
import time


def top_10_apps(df):
    """Erstellt ein interaktives und animiertes Diagramm der Top 10 Apps nach Bewertungen."""
    top_apps = df.sort_values(by="Reviews", ascending=True).head(10)  # Sortiere aufsteigend

    # Initialisiere Animation mit 0-Werten
    top_apps["Animated_Reviews"] = 0
    chart = st.empty()

    # Interaktive Auswahl für die Nutzer
    speed = st.slider("Animationsgeschwindigkeit", min_value=0.1, max_value=1.0, value=0.2, step=0.1)
    start_animation = st.button("▶️")

    if start_animation:
        # Animation durchführen (Balken wachsen langsam von 0 auf tatsächliche Werte)
        for i in range(1, 51):  # Mehr Schritte für sanftere Bewegung
            top_apps["Animated_Reviews"] = (top_apps["Reviews"] * (i / 50)).astype(int)

            fig = px.bar(
                top_apps, x="App", y="Animated_Reviews",
                title="Top 10 Apps nach Anzahl der Bewertungen",
                text_auto=True
            )
            fig.update_traces(marker_color=px.colors.qualitative.Set1, orientation='v', hoverinfo="x+y")
            fig.update_yaxes(range=[0, top_apps["Reviews"].max()], title="Anzahl der Bewertungen")
            fig.update_xaxes(title="App Name")

            chart.empty()  # Vorheriges Diagramm löschen, um doppelte IDs zu vermeiden
            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(speed / 5)
