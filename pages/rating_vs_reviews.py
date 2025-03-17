import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#  Streamlit config
st.set_page_config(layout="wide", page_title="Preis vs. Bewertung Paradoxon")


#  Load, cache, data prep
@st.cache_data
def load_data():
    """Load data, delete NaN´s, convert datetime, price categories."""

    df = pd.read_csv("google_clean_v3.csv")

    #  Delete na´s
    df = df.dropna(subset=['Rating', 'Type', 'Reviews', 'Price', 'Installs'])

    #  convert to numeric
    df['Reviews'] = df['Reviews'].astype(str).str.replace(',', '').astype(int)
    df['Installs'] = df['Installs'].astype(int)
    df['Price'] = df['Price'].astype(float)

    #  price categories function
    def categorize_price(price):
        """Categorize prices in 5 groups."""
        if price == 0:
            return "Gratis"
        elif price <= 2:
            return "Sehr Günstig (≤2€)"
        elif price <= 10:
            return "Günstig (2€ - 10€)"
        elif price <= 30:
            return "Mittelpreisig (10€ - 30€)"
        else:
            return "Teuer (>30€)"

    df["Price Category"] = df["Price"].apply(categorize_price)

    return df


#  load data for plot
plot_data = load_data()

#  title
st.title("Preis vs. Bewertung Paradoxon")
st.write(
    "Untersuchen Sie, wie Bewertungen, Rezensionen und Installationen zwischen kostenlosen und kostenpflichtigen Apps variieren.")

# layout
col_main, col_pie = st.columns([2, 1])

#  sidebar header
st.sidebar.header("Filter")

#  extreme vals filter
apply_filters = st.sidebar.checkbox("Extremwerte entfernen (Installationen > 50 Mio., Bewertungen > 10 Mio.)",
                                    value=False)
if apply_filters:
    plot_data = plot_data[(plot_data["Installs"] <= 50_000_000) & (plot_data["Reviews"] <= 10_000_000)]

#  activate log scaling
log_scale = st.sidebar.checkbox("Log-Skalierung für Bewertungen & Installationen verwenden", value=False)

# create log transformed cols
plot_data["Log Reviews"] = np.log10(plot_data["Reviews"] + 1)
plot_data["Log Installs"] = np.log10(plot_data["Installs"] + 1)

#  axis choice based on log scale selection
x_axis = "Log Reviews" if log_scale else "Reviews"
y_axis = "Log Installs" if log_scale else "Installs"

#   dot size metric
dot_size_metric = st.sidebar.selectbox("Metrik für Punktgröße wählen:", ["Reviews", "Rating", "Price", "Installs"])

#  app category filter
category_filter = st.sidebar.selectbox(
    "Kategorie wählen:",
    ["Alle"] + plot_data["Category"].unique().tolist()
)

# Apply the filter if a category is selected

if category_filter != "Alle":
    plot_data = plot_data[plot_data["Category"] == category_filter]

#  price range filter
price_range = st.sidebar.selectbox(
    "Preiskategorie wählen:",
    ["Alle", "Gratis", "Sehr Günstig (≤2€)", "Günstig (2€ - 10€)", "Mittelpreisig (10€ - 30€)", "Teuer (>30€)"]
)

#  apply price filter if not ALLE
if price_range != "Alle":
    plot_data = plot_data[plot_data["Price Category"] == price_range]

#  Scatter-Plot: Bewertungen vs. Installationen
with col_main:
    st.subheader("Scatter-Plot: Rezensionen vs. Bewertungen")

    fig_scatter = px.scatter(
        plot_data,
        x=x_axis,
        y="Rating",
        color="Type",
        size=dot_size_metric,
        title="Rezensionen vs. Bewertungen (Gratis vs. Bezahlte Apps)",
        hover_data=['App', 'Category', 'Price'],
        color_discrete_map={"Free": "#5ec962", "Paid": "#440154"},
        opacity=0.7
    )
    fig_scatter.update_traces(
        marker=dict(
            line=dict(
                color='white',  # Set the border color to white
                width=2  # Set the border width
            )
        )
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    # show filtered data

    st.dataframe(plot_data[["App", "Category", "Rating", "Reviews", "Installs", "Price", "Type"]].head())

#   pir chart
with col_pie:
    st.subheader("Bewertungsverteilung")


    #  rating categories
    def categorize_rating(rating):
        """Categorize rating in 5 groups"""
        if rating < 2:
            return "Sehr Niedrig (1.0 - 1.9)"
        elif rating < 3:
            return "Niedrig (2.0 - 2.9)"
        elif rating < 4:
            return "Mittel (3.0 - 3.9)"
        elif rating < 4.5:
            return "Hoch (4.0 - 4.4)"
        else:
            return "Sehr Hoch (4.5 - 5.0)"


    plot_data["Rating Group"] = plot_data["Rating"].apply(categorize_rating)

    # rating count by group
    rating_counts = plot_data["Rating Group"].value_counts().reset_index()
    rating_counts.columns = ["Bewertungsgruppe", "Anzahl"]

    #  pei chart for ratings
    fig_pie = px.pie(
        rating_counts,
        names="Bewertungsgruppe",
        values="Anzahl",
        title="Bewertungsverteilung (Alle Kategorien)",
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    st.plotly_chart(fig_pie, use_container_width=True)

# 3D Scatter-Plot
st.subheader("3D Scatter-Plot: Rezensionen, Installationen & Bewertungen")

fig_3d = px.scatter_3d(
    plot_data,
    x="Log Reviews" if log_scale else "Reviews",
    y="Log Installs" if log_scale else "Installs",
    z="Rating",
    color="Type",
    size=dot_size_metric,
    title="3D Scatter-Plot: Rezensionen, Installationen & Bewertungen",
    hover_data=['App'],
    color_discrete_map={"Free": "#5ec962", "Paid": "#440154"}
)

#  biggah!
fig_3d.update_layout(height=800)

st.plotly_chart(fig_3d, use_container_width=True)
