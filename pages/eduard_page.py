import pandas as pd
import streamlit as st
import plotly.express as px
import time

# Load Cleaned Data
@st.cache_data
def load_data():
    return pd.read_csv("google_clean_v2.csv")  # Use the correct dataset

df = load_data()

# Function: Top 10 Apps by Reviews
def top_10_apps(df):
    """Creates an interactive animated bar chart for the Top 10 apps by reviews."""
    df = df.copy()
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype(int)  # Convert and clean
    top_apps = df.nlargest(10, "Reviews").sort_values(by="Reviews", ascending=True)  # Top 10 ascending

    chart = st.empty()
    speed = st.slider("Animation Speed", 0.05, 1.0, 0.2, 0.05)
    start_animation = st.button("▶️ Start Animation")

    if start_animation:
        for i in range(1, 51):
            top_apps["Animated_Reviews"] = (top_apps["Reviews"] * i / 50).astype(int)
            fig = px.bar(top_apps, x="App", y="Animated_Reviews", title="Top 10 Apps by Number of Reviews",
                         text_auto=True)
            fig.update_yaxes(range=[0, max(80000000, top_apps["Reviews"].max() * 1.1)])
            chart.plotly_chart(fig, use_container_width=True)
            time.sleep(speed / 5)

# Streamlit UI
st.title("Google Play Store Analysis")

# Dropdown for selecting analysis
option = st.selectbox("Select an analysis", ["Top 10 Apps by Number of Reviews"])

# Run the selected analysis
if option == "Top 10 Apps by Number of Reviews":
    top_10_apps(df)

st.success("Analysis successfully completed.")
