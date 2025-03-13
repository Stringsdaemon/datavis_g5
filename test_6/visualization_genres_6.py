import streamlit as st
import plotly.express as px


def visualize_top_genres_by_installs(df):
    """Zeigt die Top 10 App-Genres basierend auf Installationen."""
    genres_installs = df.groupby("Genres")["Installs"].sum().reset_index()
    genres_installs = genres_installs.sort_values(by="Installs", ascending=False).head(10)

    fig = px.pie(
        genres_installs, names="Genres", values="Installs",
        title="📊 Beliebteste App-Genres basierend auf Downloads",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig, use_container_width=True)
