import streamlit as st
import plotly.express as px
import time


def animate_chart(top_apps):
    """Erstellt eine animierte Balkengrafik der Top 10 Apps nach Anzahl der Bewertungen."""
    chart = st.empty()
    speed = st.slider("🎛 Animationsgeschwindigkeit", 0.05, 1.0, 0.2, 0.05)
    start_animation = st.button("▶️ Play")

    if start_animation:
        y_max = max(1000000, top_apps["Reviews"].max() * 1.2)  # Dynamische Skalierung

        for i in range(1, 51):
            top_apps["Animated_Reviews"] = (top_apps["Reviews"] * i / 50).astype(int)
            fig = px.bar(
                top_apps, x="App", y="Animated_Reviews",
                title="📊 Top 10 Apps nach Anzahl der Bewertungen",
                text=top_apps["Animated_Reviews"].apply(lambda x: f"{x:,}"),
                color="App",
                color_discrete_sequence=px.colors.qualitative.Set2  # Moderne Farben
            )
            fig.update_traces(textposition="outside", marker=dict(line=dict(width=1, color='black')))
            fig.update_yaxes(range=[0, y_max], gridcolor='lightgray')
            fig.update_layout(
                transition_duration=300,
                plot_bgcolor='rgba(245, 245, 250, 1)',  # Heller Hintergrund
                paper_bgcolor='rgba(240, 240, 250, 1)',
                font=dict(size=14),
                height = 600, # 600/ Mindesthöhe des Diagramms setzen
                width = 800,  # 1000/ Mindestbreite des Diagramms setzen
            )

            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(speed / 5)