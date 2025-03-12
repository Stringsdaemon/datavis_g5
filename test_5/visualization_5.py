import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time


def animate_chart(top_apps):
    """Erstellt eine animierte Visualisierung der Top 10 Apps nach Anzahl der Bewertungen mit mehreren Diagrammtypen."""
    chart = st.empty()

    # Auswahl des Diagrammtyps
    chart_type = st.radio("Diagrammtyp auswählen", ["Balkendiagramm", "Kreisdiagramm", "Liniendiagramm"], index=0)

    speed = st.slider("🎛 Animationsgeschwindigkeit", 0.05, 1.0, 0.2, 0.05)
    start_animation = st.button("▶️ Play")

    if start_animation:
        y_max = max(1000000, top_apps["Reviews"].max() * 1.2)  # Dynamische Skalierung

        for i in range(1, 51):
            top_apps["Animated_Reviews"] = (top_apps["Reviews"] * i / 50).astype(int)

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
                fig = px.pie(
                    top_apps, names="App", values="Animated_Reviews",
                    title="📊 Verteilung der Bewertungen (Kreisdiagramm)",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )

            elif chart_type == "Liniendiagramm":
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=top_apps["App"],
                    y=top_apps["Animated_Reviews"],
                    mode='lines+markers',
                    line=dict(color='royalblue', width=3),
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    title="📊 Entwicklung der Bewertungen (Liniendiagramm)",
                    xaxis_title="App",
                    yaxis_title="Anzahl der Bewertungen",
                    height=600, width=800
                )

            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(speed / 5)
