import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset with caching
@st.cache_data
def load_data():
    p3_data = pd.read_csv("google_clean_v2.csv")
    p3_data = p3_data.dropna(subset=["Installs", "Content Rating"])  # Drop missing values
    p3_data["Installs"] = p3_data["Installs"].astype(int)  # Convert Installs to int
    return p3_data

p3_data = load_data()

# Streamlit UI
st.title(" Content Rating Demographics Explorer")

st.write("Analyze how installs are distributed across different content ratings.")

# Dropdown to filter content ratings
selected_ratings = st.multiselect("Select Content Ratings", p3_data["Content Rating"].unique(), default=p3_data["Content Rating"].unique())

# Filter data
filtered_p3 = p3_data[p3_data["Content Rating"].isin(selected_ratings)]

# Create stacked bar chart
fig = px.bar(
    filtered_p3,
    x="Content Rating",
    y="Installs",
    color="Category",
    title="App Installs by Content Rating",
    barmode="stack",
    hover_data=["App"]
)

# Show plot
st.plotly_chart(fig)
