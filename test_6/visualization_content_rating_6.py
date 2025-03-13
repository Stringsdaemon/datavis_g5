import streamlit as st
import plotly.express as px


def visualize_content_rating(df):
    """Visualisiert die Anzahl der Apps pro Inhaltsbewertung."""
    if df.empty:
        st.warning("⚠️ Keine Daten zum Anzeigen vorhanden! Überprüfe die Kategorie oder die Filtereinstellungen.")
        return

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
