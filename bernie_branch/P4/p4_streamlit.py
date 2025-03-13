import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset with caching
@st.cache_data
def load_data():
    df = pd.read_csv("google_clean_v2.csv")
    df = df.dropna(subset=["Last_Updated"])  # Drop missing values
    df["Last_Updated"] = pd.to_datetime(df["Last_Updated"])  # Convert to datetime
    return df

df = load_data()

# Streamlit UI
st.title("📆 Update Frequency Tracker")

st.write("Visualizing how often apps have been updated.")

# Convert min/max date to datetime.date (fix for slider)
min_date = df["Last_Updated"].min().date()
max_date = df["Last_Updated"].max().date()

# Date range slider (fix)
date_range = st.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date))

# Convert slider output back to datetime for filtering
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Filter data by selected date range
filtered_df = df[(df["Last_Updated"] >= start_date) & (df["Last_Updated"] <= end_date)]

# Count updates per day
date_counts = filtered_df["Last_Updated"].value_counts().reset_index()
date_counts.columns = ["Date", "Update Count"]

# Create heatmap
fig = px.density_heatmap(
    date_counts,
    x="Date",
    y="Update Count",
    title="App Update Frequency Over Time",
    color_continuous_scale="Viridis"
)

# Show plot
st.plotly_chart(fig)
