import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset with caching
@st.cache_data
def load_data():
    p6_data = pd.read_csv("google_clean_v2.csv")
    p6_data = p6_data.dropna(subset=["Last_Updated", "Installs"])  # Drop missing values
    p6_data["Last_Updated"] = pd.to_datetime(p6_data["Last_Updated"])  # Convert to datetime
    p6_data["Year"] = p6_data["Last_Updated"].dt.year  # Extract Year
    p6_data["Month"] = p6_data["Last_Updated"].dt.month  # Extract Month
    #  p6_data["Installs"] = p6_data["Installs"].str.replace("[+,]", "", regex=True).astype(int)  # Clean Installs
    return p6_data

p6_data = load_data()

# Streamlit UI
st.title("🔥 Time-Traveling App Popularity")

st.write("Visualizing app installs over time based on last update year/month.")

# Date filter (Year selection)
years = sorted(p6_data["Year"].unique())
selected_year = st.selectbox("Select Year", years, index=len(years)-1)  # Default to latest year

# Filter data
filtered_p6 = p6_data[p6_data["Year"] == selected_year]

# Aggregate installs by Month
install_heatmap = filtered_p6.groupby(["Month", "Year"])["Installs"].sum().reset_index()

# Pivot data for heatmap
install_pivot = install_heatmap.pivot(index="Month", columns="Year", values="Installs")

# Create heatmap
fig = px.imshow(
    install_pivot,
    labels={"x": "Year", "y": "Month", "color": "Installs"},
    title=f"📊 App Installs by Month for {selected_year}",
    color_continuous_scale="Viridis"
)

# Show plot
st.plotly_chart(fig)
