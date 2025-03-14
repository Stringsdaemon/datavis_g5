import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import time
from analysis_bottom_apps import get_bottom_10_apps_by_rating
from analysis_top_genres import get_top_10_genres_by_installs


def animate_chart(data, x_column, y_column, title, color_column, category_column=None):
    """Erstellt eine animierte Visualisierung mit mehreren Diagrammtypen."""
    chart = st.empty()
    fig = go.Figure()

    # Auswahl des Diagrammtyps
    chart_type = st.radio("Diagrammtyp auswählen", ["Balkendiagramm", "Kreisdiagramm", "Liniendiagramm"], index=0)
    speed = st.slider("🎛 Animationsgeschwindigkeit", 0.01, 1.0, 0.1, 0.01)
    if category_column:
        categories = ['Alle Kategorien'] + sorted(data[category_column].dropna().unique().tolist())
        selected_category = st.selectbox("Kategorie auswählen", categories)
        if selected_category != 'Alle Kategorien':
            data = data[data[category_column] == selected_category]

    start_animation = st.button("▶️ Play")

    if start_animation:
        y_max = max(1, data[y_column].max() * 1.2)
        animated_values = [0] * len(data)

        for i in range(1, 101):
            animated_values = (data[y_column] * i / 100).astype(float)
            data["Animated_Values"] = animated_values

            if chart_type == "Balkendiagramm":
                fig = px.bar(
                    data, x=x_column, y="Animated_Values",
                    title=title,
                    text=data["Animated_Values"].apply(lambda x: f"{x:,}"),
                    color=color_column,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig.update_traces(textposition="outside", marker=dict(line=dict(width=1, color='black')))
                fig.update_yaxes(range=[0, y_max], gridcolor='lightgray')
                fig.update_layout(height=600, width=900)  # Skalierung angepasst

            elif chart_type == "Kreisdiagramm":
                for j in range(len(data)):
                    temp_df = data.iloc[:j + 1]
                    fig = px.pie(
                        temp_df, names=x_column, values="Animated_Values",
                        title=title,
                        color_discrete_sequence=px.colors.qualitative.Set2,
                        hole=0.3
                    )
                    chart.plotly_chart(fig, use_container_width=True, key=f"chart_pie_{i}_{j}")
                    time.sleep(speed * 2)  # Langsamere Animation für bessere Sichtbarkeit
                break

            elif chart_type == "Liniendiagramm":
                fig = go.Figure()
                x_data = data[x_column].iloc[: i // 10 + 1]
                y_data = animated_values[: i // 10 + 1]
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='lines+markers',
                    line=dict(color='royalblue', width=3, shape='spline', smoothing=1.3),
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    title=title,
                    xaxis_title=x_column,
                    yaxis_title=y_column,
                    yaxis=dict(range=[0, y_max]),
                    height=600, width=900
                )
                chart.plotly_chart(fig, use_container_width=True, key=f"chart_line_{i}")
                time.sleep(speed / 2)  # Weichere Animation mit kleineren Schritten

            chart.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")
            time.sleep(speed / 5)


def visualize_bottom_apps(df):
    category_column = 'Category' if 'Category' in df.columns else None
    """Visualisiert die Top 10 Apps mit den schlechtesten Bewertungen."""
    bottom_apps = get_bottom_10_apps_by_rating(df)
    bottom_apps = bottom_apps.sort_values(by="Rating", ascending=True).head(10)
    animate_chart(bottom_apps, "App", "Rating", "👎 Top 10 Apps mit den schlechtesten Bewertungen", "App",
                  category_column)


def visualize_top_genres(df):
    category_column = 'Category' if 'Category' in df.columns else None
    """Visualisiert die Top 10 App-Genres nach Downloads."""
    top_genres = get_top_10_genres_by_installs(df)
    top_genres = top_genres.sort_values(by="Installs", ascending=False).head(10)
    animate_chart(top_genres, "Genres", "Installs", "📊 Top 10 App-Genres nach Downloads", "Genres", category_column)
