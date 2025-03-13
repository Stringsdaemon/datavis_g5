import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache_data
def load_data():
    df = pd.read_csv("google_clean_v2.csv")

    # Clean "Installs" (ensure it's treated as string first)
    df["Installs"] = df["Installs"].astype(str).str.replace("[+,]", "", regex=True).astype(float)

    # Clean "Size" (optional, but included for consistency)
    df["Size"] = df["Size"].replace("Varies with device", None)
    df["Size"] = df["Size"].astype(str).str.replace("M", "").str.replace("k", "").astype(float)

    # Drop missing values
    df = df.dropna(subset=["Rating", "Reviews", "Installs"])

    # Calculate "significance" (-log10(1/Reviews))
    df["Significance"] = -np.log10(1 / df["Reviews"])  # High reviews = high significance

    return df


df = load_data()

st.title("Review Sentiment Volcano Plot 🔥")

# Slider to filter by minimum reviews
min_reviews = st.slider(
    "Minimum Reviews",
    min_value=int(df["Reviews"].min()),
    max_value=int(df["Reviews"].max()),
    value=1000,
    help="Filter apps by minimum number of reviews"
)

# Filter data based on slider
filtered_df = df[df["Reviews"] >= min_reviews]

# Define thresholds (customize these!)
RATING_THRESHOLD = 4.0  # Apps above this are "high quality"
SIGNIFICANCE_THRESHOLD = 3.0  # Apps above this are "statistically significant"

# Create volcano plot
fig = px.scatter(
    df,
    x="Significance",
    y="Rating",
    size="Installs",
    color="Category",
    hover_name="App",
    title="True Volcano Plot: Rating vs. Significance (Reviews)",
    labels={"Significance": "-log10(1/Reviews)", "Rating": "Average Rating"},
)

# Add significance/rathing thresholds
fig.add_hline(y=RATING_THRESHOLD, line_dash="dash", line_color="red")
fig.add_vline(x=SIGNIFICANCE_THRESHOLD, line_dash="dash", line_color="green")

# Highlight "significant" apps in the top-right quadrant
highlight_df = df[
    (df["Rating"] >= RATING_THRESHOLD) &
    (df["Significance"] >= SIGNIFICANCE_THRESHOLD)
]
fig.add_trace(
    px.scatter(
        highlight_df,
        x="Significance",
        y="Rating",
        size="Installs",
        color="Category",
        hover_name="App"
    ).data[0]
)

# Customize layout
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)