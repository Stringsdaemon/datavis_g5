# Updated Streamlit Script with Improved Layout

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Streamlit Page Config
st.set_page_config(layout="wide", page_title="Price vs Rating Paradox")


# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("google_clean_v2.csv")
    df = df.dropna(subset=['Rating', 'Type', 'Reviews', 'Price', 'Installs'])

    # Convert numeric fields
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

# Page Title
st.title("Price vs Rating Paradox")
st.write("Explore how ratings, reviews, and installs differ between free and paid apps.")

# Layout: Filters on 1/3, Scatter & Bar Charts on 2/3
col_main, col_filters = st.columns([2, 1])

with col_filters:
    st.header("Filters")

    # Outlier Filter (Unchecked by default)
    apply_filters = st.checkbox("Filter extreme outliers (Installs > 50M, Reviews > 10M)", value=False)
    if apply_filters:
        p2_data = p2_data[(p2_data["Installs"] <= 50_000_000) & (p2_data["Reviews"] <= 10_000_000)]

    # Log Scaling Toggle (Unchecked by default)
    log_scale = st.checkbox("Use Log Scaling for Reviews & Installs", value=False)

    if log_scale:
        p2_data["Log Reviews"] = p2_data["Reviews"].apply(lambda x: np.log10(x + 1))
        p2_data["Log Installs"] = p2_data["Installs"].apply(lambda x: np.log10(x + 1))
        x_axis = "Log Reviews"
        y_axis = "Log Installs"
    else:
        x_axis = "Reviews"
        y_axis = "Installs"

    # Dot Size Selector
    dot_size_metric = st.selectbox("Select dot size metric:", ["Reviews", "Rating", "Price", "Installs"])

    # Price Range Selector for Paid Apps
    price_range = st.selectbox("Select a price range:",
                               ["All"] + ["Cheap (≤$5)", "Medium ($5-$20)", "Expensive (>$20)"])

    # Apply price filter if necessary
    if price_range != "All":
        p2_data = p2_data[(p2_data["Price Category"] == price_range) | (p2_data["Price"] == 0)]

with col_main:
    # Scatter Plot
    st.header("Scatter Plot: Reviews vs. Ratings")
    fig_scatter = px.scatter(
        p2_data,
        x=x_axis,
        y="Rating",
        color="Type",
        size=dot_size_metric,
        title="Reviews vs. Ratings (Free vs Paid)",
        hover_data=['App', 'Category', 'Price'],
        color_discrete_map={"Free": "blue", "Paid": "red"},
        opacity=0.7
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Bar Chart: Free vs Paid Apps by Category
    st.header("Free vs Paid Apps by Category")
    category_counts = p2_data.groupby(["Category", "Type"]).size().reset_index(name="Count")
    fig_bar = px.bar(
        category_counts,
        x="Category",
        y="Count",
        color="Type",
        title="Free vs Paid Apps by Category",
        color_discrete_map={"Free": "blue", "Paid": "red"},
        barmode="group"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Pie Chart and Category Selection Below
col_pie, col_pie_filters = st.columns([2, 1])

with col_pie_filters:
    st.header("Filter Pie Chart by Category")
    selected_category = st.selectbox("Select a category:", ["All"] + sorted(p2_data["Category"].unique()))

# Apply category filter for pie chart
if selected_category != "All":
    pie_data = p2_data[p2_data["Category"] == selected_category]
else:
    pie_data = p2_data

with col_pie:
    st.header("Ratings Distribution")


    def categorize_rating(rating):
        if rating < 2:
            return "Low (1-2)"
        elif rating < 4:
            return "Medium (3-4)"
        else:
            return "High (4.5-5)"


    pie_data["Rating Group"] = pie_data["Rating"].apply(categorize_rating)
    rating_counts = pie_data["Rating Group"].value_counts().reset_index()
    rating_counts.columns = ["Rating Group", "Count"]

    fig_pie = px.pie(
        rating_counts,
        names="Rating Group",
        values="Count",
        title=f"Ratings Distribution ({selected_category if selected_category != 'All' else 'All Categories'})",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 3D Scatter Plot Section (Expanded Height)
st.header("3D Scatter Plot: Reviews, Installs & Ratings")

fig_3d = px.scatter_3d(
    p2_data,
    x="Log Reviews" if log_scale else "Reviews",
    y="Log Installs" if log_scale else "Installs",
    z="Rating",
    color="Type",
    size=dot_size_metric,
    title="3D Scatter: Reviews, Installs & Ratings",
    hover_data=['App'],
    color_discrete_map={"Free": "blue", "Paid": "red"}
)

# Increase height of the 3D plot
fig_3d.update_layout(height=800)

st.plotly_chart(fig_3d, use_container_width=True)
