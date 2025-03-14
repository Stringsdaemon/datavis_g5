import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset (with caching for performance)
@st.cache_data
def load_data():
    df = pd.read_csv("google_clean_v2.csv")  # Load CSV
    df = df.dropna(subset=["Rating", "Category"])  # Drop missing ratings
    return df

df = load_data()

# Streamlit UI
st.title("📊 Category Rating Battle Royale")

st.write("Compare the rating distributions of two app categories.")

# Unique categories in dataset
categories = sorted(df["Category"].unique())

# Dropdown selectors
category1 = st.selectbox("Select First Category", categories, index=0)
category2 = st.selectbox("Select Second Category", categories, index=1)

# Filter data for selected categories
filtered_df = df[df["Category"].isin([category1, category2])]

# Create box plot
fig = px.violin(
    filtered_df,
    x="Category",
    y="Rating",
    color="Category",
    title=f"Rating Distribution: {category1} vs {category2}",
    points="all",  # Show individual points
    hover_data=["App"]  # Show app names on hover
)

# Display the plot
st.plotly_chart(fig)

# Summary statistics
st.write("### 📊 Summary Statistics")
st.dataframe(filtered_df.groupby("Category")["Rating"].describe().T)