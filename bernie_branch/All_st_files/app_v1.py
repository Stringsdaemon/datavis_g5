import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide", page_title="Price vs Rating Paradox")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('google_clean_v2.csv')
    df = df.dropna(subset=['Rating', 'Type', 'Reviews', 'Price', 'Installs'])

    df['Reviews'] = df['Reviews'].astype(str).str.replace(',', '').astype(int)
    df['Installs'] = df['Installs'].astype(str).str.replace('[+,]', '', regex=True).astype(int)
    df['Price'] = df['Price'].astype(float)

    # Price Range Categorization
    def categorize_price(price):
        if price == 0:
            return "Free"
        elif price <= 5:
            return "Cheap (≤$5)"
        elif price <= 20:
            return "Medium ($5-$20)"
        else:
            return "Expensive (>$20)"

    df["Price Category"] = df["Price"].apply(categorize_price)

    return df


p2_data = load_data()

# Streamlit App UI
st.title('Price vs Rating Paradox')
st.write("Analyze how ratings, reviews, and installs differ between free and paid apps.")

# **Outlier Filter Toggle**
apply_filters = st.checkbox("Filter extreme outliers (Installs > 50M, Reviews > 10M)", value=True)

if apply_filters:
    p2_data = p2_data[(p2_data["Installs"] <= 50_000_000) & (p2_data["Reviews"] <= 10_000_000)]

# **Log Scaling**
p2_data["Log Reviews"] = p2_data["Reviews"].apply(lambda x: np.log10(x + 1))
p2_data["Log Installs"] = p2_data["Installs"].apply(lambda x: np.log10(x + 1))

# **Dot Size Selector**
dot_size_metric = st.selectbox("Select dot size metric:", ["Reviews", "Rating", "Price", "Installs"])

# **Separate Paid and Free Apps**
free_apps = p2_data[p2_data["Price"] == 0]
paid_apps = p2_data[p2_data["Price"] > 0]

# **Price Range Selector for Paid Apps**
price_range = st.selectbox("Select a price range:", ["All"] + ["Cheap (≤$5)", "Medium ($5-$20)", "Expensive (>$20)"])

if price_range != "All":
    paid_apps = paid_apps[paid_apps["Price Category"] == price_range]

# **3D Scatter Plot for Paid Apps**
fig_paid = px.scatter_3d(
    paid_apps,
    x="Log Reviews",  # Log-scaled
    y="Log Installs",  # Log-scaled
    z="Rating",
    color="Price Category",
    size=dot_size_metric,
    size_max=30,
    title=f'Paid Apps (Filtered by {price_range})',
    hover_data=['App'],
    color_discrete_sequence=px.colors.sequential.Plasma
)

# **Lock Y-axis Rotation**
fig_paid.update_layout(
    #template="plotly_white",
    scene_camera=dict(
          # Orthographic projection (no perspective distortion)
        eye=dict(x=0, y=2.5, z=2.5),  # Position camera along the axis (adjust as needed)
        #center=dict(x=1.5, y=1.5, z=0.8),  # Center the view on the origin or data center
        #up=dict(x=0, y=0, z=1)  # Ensure the z-axis is "up" (standard for 2D-like views)
    ),
    scene=dict(
        xaxis=dict(showgrid=True, zeroline=True),
        yaxis=dict(showgrid=True, zeroline=True),
        zaxis=dict(showgrid=True, zeroline=True, visible=True)  # Hide the z-axis for a 2D look
    )
)

# **3D Scatter Plot for Free Apps**
fig_free = px.scatter_3d(
    free_apps,
    x="Log Reviews",
    y="Log Installs",
    z="Rating",
    color="Category",
    size=dot_size_metric,
    size_max=30,
    title="Free Apps",
    hover_data=['App'],
    color_discrete_sequence=px.colors.sequential.Viridis
)

# **Lock Y-axis Rotation**
fig_free.update_layout(
    scene=dict(
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=0.8),
            up=dict(x=0, y=0, z=1)  # Lock Y rotation at 60°
        )
    )
)

# **Combined 3D Scatter Plot for Paid vs Free**
fig_combined = px.scatter_3d(
    p2_data,
    x="Log Reviews",
    y="Log Installs",
    z="Rating",
    color="Type",
    size=dot_size_metric,
    size_max=30,
    title="Comparison: Free vs Paid Apps",
    hover_data=['App'],
    color_discrete_map={"Free": "blue", "Paid": "red"},
    symbol='Type'
)

# **Lock Y-axis Rotation**
fig_combined.update_layout(
    scene=dict(
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=0.8),
            up=dict(x=0, y=0, z=1)
        )
    )
)

# **Layout for Displaying Plots Next to Each Other**
col1, col2 = st.columns(2)

# Plot for Paid Apps in the first column
with col1:
    st.plotly_chart(fig_paid)

# Plot for Free Apps in the second column
with col2:
    st.plotly_chart(fig_free)

# Plot for Combined (Free vs Paid) under the first two
st.plotly_chart(fig_combined)
