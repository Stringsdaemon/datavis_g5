import streamlit as st
import pandas as pd
import plotly.express as px

# Set Wide Mode
st.set_page_config(page_title="Team Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("google_clean_v2.csv")  # Use the cleaned dataset

df = load_data()

# --- DATASET SUMMARY ---
st.title("Team Dashboard")
st.write("Explore the dataset before diving into individual analyses.")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Apps", len(df))
col2.metric("Average Rating", round(df["Rating"].mean(), 2))
col3.metric("Most Common Category", df["Category"].mode()[0])
col4.metric("Free vs Paid", f"{len(df[df['Price'] == 0])} Free / {len(df[df['Price'] > 0])} Paid")

# --- HISTOGRAM OF RATINGS ---
st.subheader("Ratings Distribution")
fig_hist = px.histogram(df, x="Rating", nbins=20, title="Distribution of App Ratings", color_discrete_sequence=["#1E88E5"])
st.plotly_chart(fig_hist, use_container_width=True)

# --- NAVIGATION CARDS ---
st.subheader("Explore the Analyses")
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)

with col_nav1:
    if st.button("Price vs Rating Analysis"):
        st.switch_page("pages/price_vs_rating.py")

with col_nav2:
    if st.button("Top Apps Analysis"):
        st.switch_page("pages/top_apps.py")

with col_nav3:
    if st.button("Version Analysis"):
        st.switch_page("pages/android_version.py")

with col_nav4:
    if st.button("Meow meow meow meow meow"):
        st.switch_page("pages/michael_page.py")

# --- USER GUIDE ---
with st.expander("How to Use This Dashboard"):
    st.write("""
    - **Dataset Preview:** Explore the dataset with filters.
    - **Key Insights:** See top-rated and most-reviewed apps.
    - **Analyses:** Navigate to different pages using the sidebar or buttons.
    - **Interactivity:** Use filters and animations to interact with charts.
    """)

st.success("Use the sidebar to navigate to specific analyses.")
