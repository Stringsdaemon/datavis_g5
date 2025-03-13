import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


def visualize_chart(data, chart_type):
    """Erstellt eine Visualisierung basierend auf dem ausgewählten Diagrammtyp."""
    chart = st.empty()

    if chart_type == "Balkendiagramm":
        fig = px.bar(
            data, x=data.columns[0], y=data.columns[1],
            title=f"📊 {data.columns[0]} nach {data.columns[1]}",
            text_auto=True,
            color=data.columns[0],
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(textposition="outside", marker=dict(line=dict(width=1, color='black')))
        fig.update_yaxes(gridcolor='lightgray')
        fig.update_layout(height=600, width=800)

    elif chart_type == "Kreisdiagramm":
        fig = px.pie(
            data, names=data.columns[0], values=data.columns[1],
            title=f"📊 Verteilung von {data.columns[0]}",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.3
        )

    chart.plotly_chart(fig, use_container_width=True)
