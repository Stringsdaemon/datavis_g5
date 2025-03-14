import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("google_clean_v2.csv")
    df = df.dropna(subset=["Size", "Installs"])  # Drop missing values
    df = df[df["Size"] != "Varies with device"]  # Remove non-numeric sizes
    #df["Size"] = df["Size"].str.replace("M", "").str.replace("k", "").astype(float)  # Remove M/k
    df["Size"] = df["Size"].apply(lambda x: x / 1000 if x > 100 else x)  # Convert KB to MB
    #df["Installs"] = df["Installs"].str.replace("[+,]", "", regex=True).astype(int)  # Clean installs
    return df

p7_data = load_data()

# Streamlit UI
st.title("🐝 App Size 'Sweet Spot' Finder")

st.write("Find the best app size for maximizing installs.")

# Slider to filter app size range
size_range = st.slider("Select App Size Range (MB)", min_value=0.0, max_value=500.0, value=(0.0, 500.0))

# Filter data
filtered_p7 = p7_data[(p7_data["Size"] >= size_range[0]) & (p7_data["Size"] <= size_range[1])]

# Create strip plot
fig = px.strip(
    filtered_p7,
    x="Size",
    y="Installs",
    title="📊 App Installs vs. Size",
    hover_data=["App"],
    color="Category"
)

st.plotly_chart(fig)
