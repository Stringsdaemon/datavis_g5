import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("google_clean_v2.csv")
    df = df.dropna(subset=["Rating", "Reviews", "Installs", "Type"])
    # df["Installs"] = df["Installs"].str.replace("[+,]", "", regex=True).astype(int)
    df["Reviews"] = df["Reviews"].astype(int)
    return df

p8_data = load_data()

# Normalize function
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# Aggregate data
agg_data = p8_data.groupby("Type").agg({"Rating": "mean", "Reviews": "sum", "Installs": "sum"}).reset_index()
agg_data["Normalized Rating"] = normalize(agg_data["Rating"])
agg_data["Normalized Reviews"] = normalize(np.log1p(agg_data["Reviews"]))  # Log scale for better visualization
agg_data["Normalized Installs"] = normalize(np.log1p(agg_data["Installs"]))

# Melt dataframe for radial chart
melted_p8 = agg_data.melt(id_vars=["Type"], value_vars=["Normalized Rating", "Normalized Reviews", "Normalized Installs"],
                           var_name="Metric", value_name="Value")

# Streamlit UI
st.title("🌀 Free vs. Paid App Gladiator")

st.write("Compare Free vs. Paid apps based on Ratings, Reviews, and Installs.")

# Radial chart
fig = px.line_polar(
    melted_p8,
    r="Value",
    theta="Metric",
    color="Type",
    line_close=True,
    title="📊 Free vs. Paid App Comparison"
)

st.plotly_chart(fig)
