import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Streamlit config
st.set_page_config(layout="wide", page_title="Preis vs. Bewertung Paradoxon")


#  "logo"

st.sidebar.image("assets/logo_asmodeus.jpg", use_container_width=True)


# Load, cache, data prep
@st.cache_data
def load_data():
    """Load data, delete NaN´s, convert datetime, price categories."""
    df = pd.read_csv("google_clean_v3.csv")

    # Delete na´s
    df = df.dropna(subset=['Rating', 'Type', 'Reviews', 'Price', 'Installs'])

    # Convert to numeric
    df['Reviews'] = df['Reviews'].astype(str).str.replace(',', '').astype(int)
    df['Installs'] = df['Installs'].astype(int)
    df['Price'] = df['Price'].astype(float)

    # Price categories function
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

# Load data for plot
plot_data = load_data()

# Title
st.title("Preis vs. Bewertung Paradoxon")
st.subheader("""
         Paradoxon ([ˈpaʁadoˌksɔn]):
         Definition: Eine Aussage oder Situation, die scheinbar widersprüchlich oder unlogisch erscheint, 
         aber möglicherweise eine tiefere Wahrheit enthält.
         """
          )
st.divider()
st.write(
    "Untersuchen Sie, wie Bewertungen, Rezensionen und Installationen zwischen kostenlosen und kostenpflichtigen Apps variieren.")

# Layout with new column structure
col_main, col_data = st.columns([1, 1])
col_bar, col_pie = st.columns([1, 1])

# Sidebar header
st.sidebar.header("Filter")

# Extreme vals filter
apply_filters = st.sidebar.checkbox("Extremwerte entfernen (Installationen > 50 Mio., Bewertungen > 10 Mio.)", value=False)
if apply_filters:
    plot_data = plot_data[(plot_data["Installs"] <= 50_000_000) & (plot_data["Reviews"] <= 10_000_000)]

# Activate log scaling
log_scale = st.sidebar.checkbox("Log-Skalierung für Bewertungen & Installationen verwenden", value=False)

# Create log transformed cols
plot_data["Log Reviews"] = np.log10(plot_data["Reviews"] + 1)
plot_data["Log Installs"] = np.log10(plot_data["Installs"] + 1)

# Axis choice based on log scale selection
x_axis = "Log Reviews" if log_scale else "Reviews"
y_axis = "Log Installs" if log_scale else "Installs"

# Dot size metric
dot_size_metric = st.sidebar.selectbox("Metrik für Punktgröße wählen:", ["Reviews", "Rating", "Price", "Installs"])

# App category filter
category_filter = st.sidebar.selectbox(
    "Kategorie wählen:",
    ["Alle"] + plot_data["Category"].unique().tolist()
)

# Apply the filter if a category is selected
if category_filter != "Alle":
    plot_data = plot_data[plot_data["Category"] == category_filter]

# Price range filter
price_range = st.sidebar.selectbox(
    "Preiskategorie wählen:",
    ["Alle", "Gratis", "Sehr Günstig (≤2€)", "Günstig (2€ - 10€)", "Mittelpreisig (10€ - 30€)", "Teuer (>30€)"]
)

# Apply price filter if not ALLE
if price_range != "Alle":
    plot_data = plot_data[plot_data["Price Category"] == price_range]

# Scatter-Plot: Bewertungen vs. Installationen
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


# Bar Chart: Log-Scaled Review Count per Category (Paid vs Free)
st.subheader("Log-Skalierte Rezensionen pro Kategorie (Gratis vs. Bezahlte Apps)")

# Aggregate review counts per category and type
review_counts = plot_data.groupby(["Category", "Type"])["Reviews"].sum().reset_index()

# Apply log transformation (log10)
review_counts["Log Reviews"] = np.log10(review_counts["Reviews"] + 1)  # Avoid log(0)

# Create the bar chart
fig_reviews = px.bar(
    review_counts,
    x="Category",
    y="Log Reviews",
    color="Type",
    title="Log-Skalierte Rezensionen pro Kategorie (Gratis vs. Bezahlte Apps)",
    labels={"Log Reviews": "Log₁₀(Gesamtanzahl der Rezensionen)", "Category": "Kategorie"},
    color_discrete_map={"Free": "#5ec962", "Paid": "#440154"},
    barmode="group"  # Groups Paid and Free side by side
)

# Improve layout for readability
fig_reviews.update_layout(
    xaxis_title="Kategorie",
    yaxis_title="Log₁₀(Gesamtanzahl der Rezensionen)",
    xaxis_tickangle=-45  # Rotate x-axis labels
)

# Display the chart
st.plotly_chart(fig_reviews, use_container_width=True)

# DataFrame: Show filtered data
with col_data:
    st.subheader("Daten anzeigen")
    plot_data_sorted = plot_data.sort_values(by=dot_size_metric, ascending=False)
    st.dataframe(plot_data_sorted[["App", "Category", "Rating", "Reviews", "Installs", "Price", "Type"]].head(10))

#   Bar Chart: Number of Apps per Price Category
with col_bar:
    st.subheader("Bar Chart: Anzahl der Apps nach Preis-Kategorie")

    price_counts = plot_data["Price Category"].value_counts().reset_index()
    price_counts.columns = ["Preiskategorie", "Anzahl"]

    fig_bar = px.bar(price_counts, x="Preiskategorie", y="Anzahl", title="Anzahl der Apps nach Preis-Kategorie",
                     color="Preiskategorie", color_discrete_sequence=px.colors.sequential.Plasma)

    fig_bar.update_layout(
        yaxis_title="App Count"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# Pie Chart: Rating Distribution
with col_pie:
    st.subheader("Bewertungsverteilung")

    # Rating categories
    def categorize_rating(rating):
        "Categorize rating in 5 groups"
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

    # Rating count by group
    rating_counts = plot_data["Rating Group"].value_counts().reset_index()
    rating_counts.columns = ["Bewertungsgruppe", "Anzahl"]

    # Pie chart for ratings
    fig_pie = px.pie(
        rating_counts,
        names="Bewertungsgruppe",
        values="Anzahl",
        title="Bewertungsverteilung (Alle Kategorien)",
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    st.plotly_chart(fig_pie, use_container_width=True)

#   Pivot Table: Reviews per Category (Paid vs Free)
st.subheader("Tabelle der Rezensionen pro Kategorie (Gratis vs. Bezahlte Apps)")

#  aggregate reviews by cat and type
review_table = plot_data.groupby(["Category", "Type"])["Reviews"].sum().unstack(fill_value=0)

#  add total column (Paid Free sum)
review_table["Total"] = review_table.sum(axis=1)

# Convert to integer format for display
review_table = review_table.astype(int).sort_values(by="Total", ascending=False)

# Display as Streamlit table
st.dataframe(review_table.style.format(thousands=","))  # Formats numbers with commas for readability


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

# Bigger!
fig_3d.update_layout(height=1200)

st.plotly_chart(fig_3d, use_container_width=True)


