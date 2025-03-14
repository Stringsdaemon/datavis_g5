import pandas as pd
import streamlit as st
import plotly.express as px
import time


def top_10_apps(df):
    """Erstellt ein interaktives und animiertes Diagramm der Top 10 Apps nach Bewertungen."""
    df = df.copy()
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype(int)  # Konvertiere und bereinige
    top_apps = df.nlargest(10, "Reviews").sort_values(by="Reviews", ascending=True)  # Top 10 aufsteigend

    chart = st.empty()
    speed = st.slider("Animationsgeschwindigkeit", 0.05, 1.0, 0.2, 0.05)
    start_animation = st.button("▶️")

    if start_animation:
        for i in range(1, 51):
            top_apps["Animated_Reviews"] = (top_apps["Reviews"] * i / 50).astype(int)
            fig = px.bar(top_apps, x="App", y="Animated_Reviews", title="Top 10 Apps nach Anzahl der Bewertungen",
                         text_auto=True)
            fig.update_yaxes(range=[0, max(80000000, top_apps["Reviews"].max() * 1.1)])
            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(speed / 5)
