import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import numpy as np
import os

# Daten laden mit Fehlerhandling
def load_data():
    file_path = "google_clean_v2.csv"
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Die Datei {file_path} wurde nicht gefunden.")
        df = pd.read_csv(file_path)
        if "Price" not in df.columns or df["Price"].isnull().all():
            raise ValueError("Die Spalte 'Price' ist leer oder fehlt.")
        if "Installs" not in df.columns or df["Installs"].isnull().all():
            raise ValueError("Die Spalte 'Installs' ist leer oder fehlt.")
        df["Price"] = pd.to_numeric(df["Price"].astype(str).str.replace("$", ""), errors="coerce")
        df["Installs"] = pd.to_numeric(df["Installs"].astype(str).str.replace(",", "").str.replace("+", ""), errors="coerce")
    except Exception as e:
        st.error(f"Fehler beim Lesen der Daten: {e}")



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
        y_max = max(1000000, top_apps.iloc[:, 1].max() * 1.2)

        if chart_type == "3D Bubble Chart":
            for i in range(1, 101):
                animated_factor = i / 100
                top_apps["Animated_Column"] = pd.to_numeric(top_apps.iloc[:, 1], errors="coerce").fillna(
                    0) * animated_factor
                top_apps["Size"] = (top_apps["Animated_Column"] / top_apps["Animated_Column"].max()) * 50

                fig = px.scatter_3d(
                    top_apps, x="App", y="Animated_Column", z="Animated_Column",
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
            y_data = pd.to_numeric(top_apps.iloc[:, 1], errors="coerce").fillna(0)

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
                    title="📊 Entwicklung der Werte",
                    xaxis_title="App",
                    yaxis_title="Werte",
                    yaxis=dict(range=[0, y_max]),
                    height=800, width=1000
                )
                chart.plotly_chart(fig, use_container_width=True, key=f"chart_line_{j}")
                time.sleep(1 / (speed * 30))
            return

        for i in range(1, 101):
            animated_column = pd.to_numeric(top_apps.iloc[:, 1], errors="coerce").fillna(0) * (i / 100)
            top_apps["Animated_Column"] = animated_column

            if chart_type == "Balkendiagramm":
                fig = px.bar(
                    top_apps, x="App", y="Animated_Column",
                    title="📊 Balkendiagramm der Werte",
                    text=top_apps["Animated_Column"].apply(lambda x: f"{x:,}"),
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
                        temp_df, names="App", values="Animated_Column",
                        title="📊 Kreisdiagramm der Werte",
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        hole=0.3
                    )
                    chart.plotly_chart(fig, use_container_width=True, key=f"chart_pie_{i}_{j}")
                    time.sleep(1 / (speed * 30))
                break

            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(1 / (speed * 30))
        return


# Funktionen für Installations- und Kostendaten

def get_installation_data(df, category):
    df = df.copy()
    df["Installs"] = pd.to_numeric(df["Installs"].str.replace(",", "").str.replace("+", ""), errors="coerce").fillna(
        0).astype(int)

    if category != "Alle Kategorien":
        df = df[df["Category"] == category]

    top_installs = df.sort_values(by="Installs", ascending=False).drop_duplicates(subset=["App"]).head(10)
    top_installs = top_installs.sort_values(by="Installs", ascending=True)

    return top_installs


def get_cost_comparison_data(df, category):
    df = df.copy()
    df["Price"] = pd.to_numeric(df["Price"].str.replace("$", ""), errors="coerce").fillna(0).astype(float)

    if category != "Alle Kategorien":
        df = df[df["Category"] == category]

    top_costs = df.sort_values(by="Price", ascending=False).drop_duplicates(subset=["App"]).head(10)
    top_costs = top_costs.sort_values(by="Price", ascending=True)

    return top_costs


# Streamlit UI
df = load_data()
st.markdown("#### 📊 Google Play Store Analyse", unsafe_allow_html=True)
st.markdown("###### Entdecke deine App")

categories = ["Alle Kategorien"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.selectbox("📂 Wähle eine Kategorie", categories, key="category_select")

option = st.selectbox("📈 Wähle eine Analyse",
                      ["Top 10 Apps nach Anzahl der Bewertungen", "Installationszahlen", "Kostenvergleich"])

if option == "Top 10 Apps nach Anzahl der Bewertungen":
    top_apps = get_top_10_apps(df, selected_category)

    if not top_apps.empty:
        animate_chart(top_apps)
    else:
        st.warning("⚠️ Keine Apps in dieser Kategorie gefunden.")

elif option == "Installationszahlen":
    top_installs = get_installation_data(df, selected_category)

    if not top_installs.empty:
        animate_chart(top_installs)
    else:
        st.warning("⚠️ Keine Apps mit Installationszahlen in dieser Kategorie gefunden.")

elif option == "Kostenvergleich":
    top_costs = get_cost_comparison_data(df, selected_category)

    if not top_costs.empty:
        animate_chart(top_costs)
    else:
        st.warning("⚠️ Keine kostenpflichtigen Apps in dieser Kategorie gefunden.")
