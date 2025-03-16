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

# Title and Description
st.title('Price vs Rating Paradox')
st.write("Explore how ratings, reviews, and installs differ between free and paid apps.")

# **Filters**
apply_filters = st.checkbox("Filter extreme outliers (Installs > 50M, Reviews > 10M)", value=True)
if apply_filters:
    p2_data = p2_data[(p2_data["Installs"] <= 50_000_000) & (p2_data["Reviews"] <= 10_000_000)]

# Log Scaling Toggle
log_scale = st.checkbox("Use Log Scaling for Reviews & Installs", value=True)

if log_scale:
    p2_data["Log Reviews"] = p2_data["Reviews"].apply(lambda x: np.log10(x + 1))
    p2_data["Log Installs"] = p2_data["Installs"].apply(lambda x: np.log10(x + 1))
    x_axis = "Log Reviews"
    y_axis = "Log Installs"
else:
    x_axis = "Reviews"
    y_axis = "Installs"

# **Dot Size Selector**
dot_size_metric = st.selectbox("Select dot size metric:", ["Reviews", "Rating", "Price", "Installs"])

# **Price Range Selector for Paid Apps**
price_range = st.selectbox("Select a price range:", ["All"] + ["Cheap (≤$5)", "Medium ($5-$20)", "Expensive (>$20)"])

# Apply price filter if necessary
if price_range != "All":
    p2_data = p2_data[(p2_data["Price Category"] == price_range) | (p2_data["Price"] == 0)]

# **2D Scatter Plot (Main Visualization)**
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

# **Side Table: Top Apps Based on Reviews or Rating**
st.sidebar.header("📌 Top Apps Table")
sort_metric = st.sidebar.radio("Sort by:", ["Most Reviewed", "Highest Rated"])

if sort_metric == "Most Reviewed":
    top_apps = p2_data.sort_values(by="Reviews", ascending=False).head(10)
else:
    top_apps = p2_data.sort_values(by="Rating", ascending=False).head(10)

st.sidebar.dataframe(top_apps[["App", "Category", "Rating", "Reviews", "Price"]])

# **Bar Chart: Free vs Paid Apps per Category**
category_counts = p2_data.groupby(["Category", "Type"]).size().reset_index(name="Count")
fig_bar = px.bar(
    category_counts,
    x="Category",
    y="Count",
    color="Type",
    title="📊 Free vs Paid Apps by Category",
    color_discrete_map={"Free": "blue", "Paid": "red"},
    barmode="group"
)

# **Pie Chart (Retained)**
def categorize_rating(rating):
    if rating < 2:
        return "Low (1-2)"
    elif rating < 4:
        return "Medium (3-4)"
    else:
        return "High (4.5-5)"

p2_data["Rating Group"] = p2_data["Rating"].apply(categorize_rating)
rating_counts = p2_data["Rating Group"].value_counts().reset_index()
rating_counts.columns = ["Rating Group", "Count"]

fig_pie = px.pie(
    rating_counts,
    names="Rating Group",
    values="Count",
    title="Ratings Distribution",
    color_discrete_sequence=px.colors.sequential.Viridis
)

# **Streamlit Layout**
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.plotly_chart(fig_bar, use_container_width=True)

st.plotly_chart(fig_pie, use_container_width=True)

# **Bonus: 3D Scatter Plot at the Bottom**
fig_3d = px.scatter_3d(
    p2_data,
    x="Log Reviews" if log_scale else "Reviews",
    y="Log Installs" if log_scale else "Installs",
    z="Rating",
    color="Type",
    size=dot_size_metric,
    title="🌍 3D Scatter: Reviews, Installs & Ratings",
    hover_data=['App'],
    color_discrete_map={"Free": "blue", "Paid": "red"}
)

st.plotly_chart(fig_3d, use_container_width=True)

