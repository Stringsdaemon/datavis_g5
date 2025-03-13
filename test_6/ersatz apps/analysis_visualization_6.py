import streamlit as st
import plotly.express as px
import pandas as pd


def visualize_content_rating(df):
    """Visualisiert die Anzahl der Apps pro Inhaltsbewertung."""
    content_rating_counts = df["Content Rating"].value_counts().reset_index()
    content_rating_counts.columns = ["Content Rating", "Anzahl"]

    fig = px.bar(
        content_rating_counts, x="Content Rating", y="Anzahl",
        title="📊 Anzahl der Apps pro Inhaltsbewertung",
        color="Content Rating",
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def visualize_bottom_10_apps(df):
    """Zeigt die 10 Apps mit den schlechtesten Bewertungen."""
    df_sorted = df.sort_values(by="Rating", ascending=True).head(10)

    fig = px.bar(
        df_sorted, x="App", y="Rating",
        title="📉 Top 10 Apps mit den schlechtesten Bewertungen",
        color="App",
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


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
