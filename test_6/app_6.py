import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time


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
    chart_type = st.radio("Diagrammtyp auswählen", ["Balkendiagramm", "Kreisdiagramm", "Liniendiagramm"], index=0)

    speed = st.slider("🎛 Animationsgeschwindigkeit", 0.01, 1.0, 0.1, 0.01)
    start_animation = st.button("▶️ Play")

    if start_animation:
        y_max = max(1000000, top_apps["Reviews"].max() * 1.2)  # Dynamische Skalierung
        animated_reviews = [0] * len(top_apps)

        for i in range(1, 101):  # Mehr Schritte für weichere Animation
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
                fig.update_layout(height=600, width=800)

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
                    time.sleep(speed * 5)
                break

            elif chart_type == "Liniendiagramm":
                fig = go.Figure()
                x_data = top_apps["App"]
                y_data = top_apps["Reviews"]

                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data * (i / 100),
                    mode='lines',
                    line=dict(color='royalblue', width=3, shape='spline', smoothing=1.3)
                ))
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='markers',
                    marker=dict(size=8, color='royalblue')
                ))
                fig.update_layout(
                    title="📊 Entwicklung der Bewertungen (Liniendiagramm)",
                    xaxis_title="App",
                    yaxis_title="Anzahl der Bewertungen",
                    yaxis=dict(range=[0, y_max]),
                    height=600, width=800
                )
                chart.plotly_chart(fig, use_container_width=True, key=f"chart_line_{i}")
                time.sleep(speed / 2)

            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(speed / 5)


# Streamlit UI
df = load_data()
st.title("📊 Google Play Store Analyse")
st.markdown("### Entdecke die beliebtesten Apps nach Bewertungen")

# Kategorien-Auswahl
categories = ["Alle Kategorien"] + sorted(df["Category"].dropna().unique().tolist())
selected_category = st.selectbox("📂 Wähle eine Kategorie", categories, key="category_select")

# Auswahl für Analyse
option = st.selectbox("📈 Wähle eine Analyse", ["Top 10 Apps Anzahl der Bewertungen"])

if option == "Top 10 Apps Anzahl der Bewertungen":
    st.markdown(f"### 📱 Top 10 Apps in der Kategorie: **{selected_category}**")
    st.markdown("\nDie Balkenanimation zeigt, wie viele Bewertungen die Top-Apps erhalten haben.")

    # Lade die Top 10 Apps für die gewählte Kategorie
    top_apps = get_top_10_apps(df, selected_category)

    if not top_apps.empty:
        animate_chart(top_apps)
    else:
        st.warning("⚠️ Keine Apps in dieser Kategorie gefunden.")
