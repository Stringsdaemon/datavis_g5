import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import numpy as np
import os

st.set_page_config(page_title="Top apps study", layout="wide")

#  "logo"

st.sidebar.image("assets/logo_asmodeus.jpg", use_container_width=True)


# Daten laden mit Fehlerhandling
def load_data():
    file_path = "google_clean_v3.csv"
    if not os.path.exists(file_path):
        st.error("⚠️ Die Datei google_clean_v3.csv wurde nicht gefunden.")
        return pd.DataFrame()
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"⚠️ Fehler beim Laden der Datei: {e}")
        return pd.DataFrame()


# Funktion zur Auswahl der Top 10 Apps
def get_top_10_apps(df, category):
    df = df.copy()
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype(int)

    if category != "Alle Kategorien":
        df = df[df["Category"] == category]

    top_apps = df.sort_values(by="Reviews", ascending=False).drop_duplicates(subset=["App"]).head(10)
    top_apps = top_apps.sort_values(by="Reviews", ascending=True)

    return top_apps


# Hauptanimationsfunktion
def animate_chart(top_apps):
    chart = st.empty()
    chart_type = st.radio("Diagrammtyp auswählen",
                          ["Balkendiagramm", "Kreisdiagramm", "Liniendiagramm", "3D Bubble Chart"], index=0)
    speed = st.slider("🎛 Animationsgeschwindigkeit", 0.01, 1.0, 1.0, 0.01)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_animation = st.button("▶️ Play", key="start_button", help="Starte die Animation")

    if start_animation:
        y_max = max(1000000, top_apps["Reviews"].max() * 1.2)

        if chart_type == "3D Bubble Chart":
            for i in range(1, 101):
                animated_factor = i / 100
                top_apps["Animated_Reviews"] = (top_apps["Reviews"] * animated_factor).astype(int)
                top_apps["Size"] = (top_apps["Animated_Reviews"] / top_apps["Reviews"].max()) * 50

                fig = px.scatter_3d(
                    top_apps, x="App", y="Animated_Reviews", z="Animated_Reviews",
                    size="Size", color="App",
                    title="📊 3D Bubble Chart der Top 10 Apps",
                    opacity=0.8,
                    size_max=50
                )
                fig.update_traces(marker=dict(sizemode='area', sizemin=5))
                fig.update_layout(
                    dragmode='pan',
                    scene_camera=dict(
                        eye=dict(x=1.5 - animated_factor, y=1.5 - animated_factor, z=0.5 + animated_factor)),
                    scene=dict(
                        xaxis=dict(range=[-1, len(top_apps) + 1]),
                        yaxis=dict(range=[0, y_max]),
                        zaxis=dict(range=[0, y_max])
                    )
                )
                chart.plotly_chart(fig, use_container_width=True, key=f"chart_3d_{i}")
                time.sleep(1 / (speed * 30))
            return

        if chart_type == "Liniendiagramm":
            fig = go.Figure()
            x_data = top_apps["App"]
            y_data = top_apps["Reviews"]

            for j in range(1, len(x_data) + 1):
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=x_data[:j],
                    y=y_data[:j],
                    mode='lines+markers',
                    line=dict(color='royalblue', width=3),
                    marker=dict(size=8, color='royalblue')
                ))
                fig.update_layout(
                    dragmode='pan',
                    title="📊 Entwicklung der Bewertungen (Liniendiagramm)",
                    xaxis_title="App",
                    yaxis_title="Anzahl der Bewertungen",
                    yaxis=dict(range=[0, y_max]),
                    height=800, width=1000
                )
                chart.plotly_chart(fig, use_container_width=True, key=f"chart_line_{j}")
                time.sleep(1 / (speed * 30))
            return

        for i in range(1, 101):
            animated_reviews = (top_apps["Reviews"] * i / 100).astype(int)
            top_apps["Animated_Reviews"] = animated_reviews

            if chart_type == "Balkendiagramm":
                fig = px.bar(
                    top_apps, x="App", y="Animated_Reviews",
                    title="📊 Top 10 Apps nach Anzahl der Bewertungen",
                    text=top_apps["Animated_Reviews"].apply(lambda x: f"{x:,}"),
                    color="App",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig.update_traces(textposition="outside", marker=dict(line=dict(width=1, color='black')))
                fig.update_yaxes(range=[0, y_max], gridcolor='lightgray')
                fig.update_layout(
                    dragmode='pan', height=600, width=800)

            elif chart_type == "Kreisdiagramm":
                fig = go.Figure()
                for j in range(len(top_apps)):
                    temp_df = top_apps.iloc[:j + 1]
                    fig = px.pie(
                        temp_df, names="App", values="Animated_Reviews",
                        title="📊 Verteilung der Bewertungen (Kreisdiagramm)",
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        hole=0.3
                    )
                    chart.plotly_chart(fig, use_container_width=True, key=f"chart_pie_{i}_{j}")
                    time.sleep(1 / (speed * 30))
                break

            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(1 / (speed * 30))


# Streamlit UI
df = load_data()
st.markdown("#### 📊 Google Play Store Analyse", unsafe_allow_html=True)
st.markdown("###### Entdecke deine App")

categories = ["Alle Kategorien"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.selectbox("📂 Wähle eine Kategorie", categories, key="category_select")

option = st.selectbox("📈 Wähle eine Analyse", ["Top 10 Apps nach Anzahl der Bewertungen"])

if option == "Top 10 Apps nach Anzahl der Bewertungen":
    top_apps = get_top_10_apps(df, selected_category)

    if not top_apps.empty:
        animate_chart(top_apps)
    else:
        st.warning("⚠️ Keine Apps in dieser Kategorie gefunden.")
