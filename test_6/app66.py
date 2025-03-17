import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime

# Daten laden und bereinigen
def load_data():
    file_path = "google_clean_v2.csv"
    return pd.read_csv(file_path)

def get_top_10_apps(df, category):
    """Filtert die Top 10 Apps nach Bewertungen basierend auf der ausgewählten Kategorie."""
    df = df.copy()
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype(int)

    # Filter nach Kategorie
    if category != "Alle Kategorien":
        df = df[df["Category"] == category]

    # Entferne doppelte Apps und nehme nur die höchsten Bewertungen pro App
    top_apps = df.sort_values(by="Reviews", ascending=False).drop_duplicates(subset=["App"]).head(10)
    top_apps = top_apps.sort_values(by="Reviews", ascending=True)  # Sortiere für Animation

    return top_apps

def animate_chart(top_apps):
    """Erstellt eine animierte Visualisierung der Top 10 Apps nach Anzahl der Bewertungen mit mehreren Diagrammtypen."""
    chart = st.empty()

    # Auswahl des Diagrammtyps
    chart_type = st.radio("Diagrammtyp auswählen",
                          ["Balkendiagramm", "3D Balkendiagramm", "Kreisdiagramm", "Liniendiagramm", "3D Bubble Chart"], index=0)

    speed = st.slider("🎛 Animationsgeschwindigkeit", 0.01, 1.0, 0.3, 0.01)  # Langsamere Standardgeschwindigkeit
    play_pause = st.toggle("▶️ Play / ⏸ Pause", value=False)

    if not play_pause or top_apps.empty:
        return  # Warten, bis Play gedrückt wird

    y_max = max(1000000, top_apps["Reviews"].max() * 1.2)  # Dynamische Skalierung

    if chart_type == "3D Bubble Chart":
        for i in range(1, 101):
            top_apps["Animated_Reviews"] = (top_apps["Reviews"] * i / 100).astype(int)
            fig = px.scatter_3d(
                top_apps, x="App", y="Animated_Reviews", z="Animated_Reviews",
                size="Animated_Reviews", color="App",
                title="📊 3D Bubble Chart der Top 10 Apps",
                opacity=0.8, size_max=50
            )
            fig.update_layout(scene=dict(zaxis=dict(range=[0, y_max])))
            chart.plotly_chart(fig, use_container_width=True)
            time.sleep(speed / 3)
        return

    for i in range(1, 101):
        animated_reviews = (top_apps["Reviews"] * i / 100).astype(int)
        top_apps["Animated_Reviews"] = animated_reviews

        if chart_type == "3D Balkendiagramm":
            fig = go.Figure()
            for idx, row in top_apps.iterrows():
                fig.add_trace(go.Scatter3d(
                    x=[row["App"], row["App"]],
                    y=[idx, idx],
                    z=[0, row["Animated_Reviews"]],
                    mode="lines",
                    line=dict(color="blue", width=10),
                    name=row["App"]
                ))
            fig.update_layout(
                title="📊 3D Balkendiagramm der Top 10 Apps",
                scene=dict(
                    xaxis_title="App",
                    yaxis_title="Index",
                    zaxis_title="Anzahl der Bewertungen",
                    zaxis=dict(range=[0, y_max])
                ),
                height=600, width=800
            )
            chart.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Balkendiagramm":
            fig = px.bar(
                top_apps, x="App", y="Animated_Reviews",
                title="📊 Top 10 Apps nach Anzahl der Bewertungen",
                text=top_apps["Animated_Reviews"].apply(lambda x: f"{x:,}"),
                color="App",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_traces(textposition="outside", marker=dict(line=dict(width=1, color='black')))
            fig.update_yaxes(range=[0, y_max], gridcolor='lightgray')
            fig.update_layout(height=600, width=800)
        elif chart_type == "Kreisdiagramm":
            fig = px.pie(
                top_apps, names="App", values="Animated_Reviews",
                title="📊 Verteilung der Bewertungen (Kreisdiagramm)",
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.3
            )
        elif chart_type == "Liniendiagramm":
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=top_apps["App"],
                y=top_apps["Animated_Reviews"],
                mode='lines+markers',
                line=dict(color='royalblue', width=3),
                marker=dict(size=8, color='royalblue')
            ))
            fig.update_layout(
                title="📊 Entwicklung der Bewertungen (Liniendiagramm)",
                xaxis_title="App",
                yaxis_title="Anzahl der Bewertungen",
                yaxis=dict(range=[0, y_max]),
                height=800, width=1000
            )
        chart.plotly_chart(fig, use_container_width=True)
        time.sleep(speed / 5)

# Streamlit UI
df = load_data()
st.markdown("# 📊 Google Play Store Analyse", unsafe_allow_html=True)
st.markdown("### Entdecke die beliebtesten Apps nach Bewertungen")

# Kategorien-Auswahl
categories = ["Alle Kategorien"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.selectbox("📂 Wähle eine Kategorie", categories, key="category_select")

# Auswahl für Analyse
option = st.selectbox("📈 Wähle eine Analyse", ["Top 10 Apps nach Anzahl der Bewertungen"])

if option == "Top 10 Apps nach Anzahl der Bewertungen":
    top_apps = get_top_10_apps(df, selected_category)
    if not top_apps.empty:
        animate_chart(top_apps)
    else:
        st.warning("⚠️ Keine Apps in dieser Kategorie gefunden.")
