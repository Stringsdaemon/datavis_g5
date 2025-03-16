import streamlit as st
import pandas as pd
import plotly.express as px


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
    x="Reviews",
    y="Installs",
    z="Rating",
    color="Price Category",
    size=dot_size_metric,
    size_max=30,
    title=f'Paid Apps (Filtered by {price_range})',
    hover_data=['App'],
    color_discrete_sequence=px.colors.sequential.Plasma
)

# **3D Scatter Plot for Free Apps**
fig_free = px.scatter_3d(
    free_apps,
    x="Reviews",
    y="Installs",
    z="Rating",
    color="Category",
    size=dot_size_metric,
    size_max=30,
    title="Free Apps",
    hover_data=['App'],
    color_discrete_sequence=px.colors.sequential.Viridis
)

# **Combined 3D Scatter Plot for Paid vs Free**
fig_combined = px.scatter_3d(
    p2_data,
    x="Reviews",
    y="Installs",
    z="Rating",
    color="Type",
    size=dot_size_metric,
    size_max=30,
    title="Comparison: Free vs Paid Apps",
    hover_data=['App'],
    color_discrete_map={"Free": "blue", "Paid": "red"}
)

# **Display Plots**
st.plotly_chart(fig_paid)
st.plotly_chart(fig_free)
st.plotly_chart(fig_combined)
