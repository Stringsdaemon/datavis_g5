import streamlit as st
import plotly.express as px


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
