import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time


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
                    time.sleep(speed * 5)  # Viel langsamere, sichtbare Animation
                break

            elif chart_type == "Liniendiagramm":
                fig = go.Figure()
                x_data = top_apps["App"].iloc[: i // 10 + 1]
                y_data = animated_reviews[: i // 10 + 1]

                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='lines+markers',
                    line=dict(color='royalblue', width=3, shape='spline', smoothing=1.3),  # Weiche Linien
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    title="📊 Entwicklung der Bewertungen (Liniendiagramm)",
                    xaxis_title="App",
                    yaxis_title="Anzahl der Bewertungen",
                    yaxis=dict(range=[0, y_max]),
                    height=600, width=800
                )
                chart.plotly_chart(fig, use_container_width=True, key=f"chart_line_{i}")
                time.sleep(speed / 2)  # Sanftere Animation mit kleineren Schritten

            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(speed / 5)
