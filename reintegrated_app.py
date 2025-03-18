import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid


# Set Wide Mode
st.set_page_config(page_title="Gruppe 5 Datenvisualisierung", layout="wide")

#  "logo"

# Inject CSS to hide sidebar navigation
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("assets/logo_asmodeus.jpg", use_container_width=True)

# Custom page navigation
page = st.sidebar.radio("Go to:", ["Home", "Analytics", "Settings"])

# Display content based on selection
if page == "Home":
    st.title("🏠 Welcome to Home Page!")
elif page == "Analytics":
    st.title("📊 Analytics Dashboard")
elif page == "Settings":
    st.title("⚙️ Settings")
# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("google_clean_v3.csv")  # Use the cleaned dataset
    df["Last_Updated"] = pd.to_datetime(df["Last_Updated"], errors="coerce", format="%Y-%m-%d")  # Fix date parsing
    return df

df = load_data()

# --- DATASET SUMMARY ---
st.title("Google Play Store Datenvisualisierung")
st.write(
    """
    This dataset explores different metrics of the many apps offered in the Google Play Store like total number 
    of reviews or installs, the rating of the app and the date of the last update.

    The data set contains a total of 10840 entries spread across 16 columns. This dataset found in Kaggle has already
    been passed through a cleaning process, the only extra work we did was re-joining the date columns into its 
    original column, [Last_Updated]
    """
)

# --- METRICS ---
col1, col2, col3, col4 = st.columns(4)
# Custom function to display the metric inside a styled box
def styled_metric(label, value):
    return f"""
    <div style="border: 2px solid #440154; border-radius: 10px; padding: 15px; background-color: #e98eff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
        <h3 style="text-align: center; font-size: 20px; font-weight: bold; color: #440154;">{label}</h3>
        <p style="text-align: center; font-size: 24px; font-weight: bold; color: #440154;">{value}</p>
    </div>
    """

# Display the styled metrics in columns
col1.markdown(styled_metric("Total Apps", len(df)), unsafe_allow_html=True)
col2.markdown(styled_metric("Average Rating", round(df["Rating"].mean(), 2)), unsafe_allow_html=True)
col3.markdown(styled_metric("Most Common Category", df["Category"].mode()[0]), unsafe_allow_html=True)
col4.markdown(styled_metric("Free vs Paid", f"{len(df[df['Type'] == 'Free'])} Free / {len(df[df['Type'] == 'Paid'])} Paid"), unsafe_allow_html=True)

# --- FILTERS ---
st.sidebar.header("🔍 Filter Dataset")

# Select specific columns for filtering
selected_type = st.sidebar.selectbox("Select Type", ["All"] + df["Type"].unique().tolist())  # Add 'All' option
selected_category = st.sidebar.selectbox("Select Category", ["All"] + df["Category"].unique().tolist())  # Add 'All' option
selected_rating = st.sidebar.slider("Select Rating Range", min_value=0.0, max_value=5.0, value=(0.0, 5.0))
selected_reviews = st.sidebar.slider("Select Reviews Range", min_value=0, max_value=int(df["Reviews"].max()), value=(0, int(df["Reviews"].max())))

# Apply filters based on user input
df_filtered = df[
    ((df["Type"] == selected_type) | (selected_type == "All")) &  # Include 'All' option for Type
    ((df["Category"] == selected_category) | (selected_category == "All")) &  # Include 'All' option for Category
    (df["Rating"] >= selected_rating[0]) &
    (df["Rating"] <= selected_rating[1]) &
    (df["Reviews"] >= selected_reviews[0]) &
    (df["Reviews"] <= selected_reviews[1])
]

# --- DATASET EXPLORATION ---
st.subheader("📊 Dataset Exploration")
# Display the filtered dataframe using AgGrid
AgGrid(df_filtered)

# ------full dataset preview charts-----

col_main_chart1, col_main_chart2 = st.columns(2)

# Main Chart 1
with col_main_chart1:
    # Create a bar chart of the average ratings per category
    avg_ratings = df_filtered.groupby("Category")["Rating"].mean().sort_values(ascending=False)
    fig_category_ratings = px.bar(avg_ratings, x=avg_ratings.index, y=avg_ratings.values,
                                  title="Average Ratings per Category",
                                  color=avg_ratings.values,  # Apply color based on the average ratings
                                  color_continuous_scale="Viridis"  # Apply Viridis color scale
    )
    fig_category_ratings.update_layout(
        yaxis_title="Average Rating"  # Correct y-axis title
    )
    st.plotly_chart(fig_category_ratings, use_container_width=True)

    # Show DataFrame preview for this plot
    st.subheader("Data Preview for Average Ratings per Category")
    st.write(df_filtered.groupby("Category")["Rating"].mean().head())  # Display top 5 rows of the grouped data

# Main Chart 2
with col_main_chart2:
    # Create a bar chart of installs per category (if 'Installs' column exists)
    if "Installs" in df.columns:
        installs_per_category = df_filtered.groupby("Category")["Installs"].sum().sort_values(ascending=False)
        fig_installs = px.bar(installs_per_category, x=installs_per_category.index, y=installs_per_category.values,
                              title="Total Installs per Category",
                              color=avg_ratings.values,  # Apply color based on the average ratings
                              color_continuous_scale="Viridis"  # Apply Viridis color scale
        )
        fig_installs.update_layout(
            yaxis_title="Total Installs"  # Correct y-axis title
        )
        st.plotly_chart(fig_installs, use_container_width=True)

        # Show DataFrame preview for this plot
        st.subheader("Data Preview for Installs per Category")
        st.write(installs_per_category.head())  # Display top 5 rows of the grouped data

# --- CHART CONTAINER (Custom Visualizations) ---
st.subheader("Quick Analysis")

# Create three columns in a row for charts
col_chart1, col_chart2, col_chart3 = st.columns(3)

# Chart 1: Distribution of Ratings
with col_chart1:
    # Create a histogram of Ratings Distribution
    fig_hist = px.histogram(df_filtered, x="Rating", nbins=20, title="Distribution of App Ratings", color_discrete_sequence=["#5ec962"])
    st.plotly_chart(fig_hist, use_container_width=True)

    # Show DataFrame preview for this plot
    st.subheader("Data Preview for Ratings Distribution")
    st.write(df_filtered[["App", "Rating"]].head())  # Display top 5 rows of relevant data

# Chart 3: Top 10 Most Reviewed Apps
with col_chart2:
    # Create a bar chart of the top 10 most reviewed apps
    top_reviewed = df_filtered.nlargest(10, "Reviews")
    fig_top_reviews = px.bar(top_reviewed, x="App", y="Reviews", title="Top 10 Most Reviewed Apps", color="Reviews", color_continuous_scale="Viridis")
    st.plotly_chart(fig_top_reviews, use_container_width=True)

    # Show DataFrame preview for this plot
    st.subheader("Data Preview for Top 10 Most Reviewed Apps")
    st.write(top_reviewed[["App", "Reviews"]].head())  # Display top 5 rows of relevant data

# Chart 3: rating vs reviews
with col_chart3:
    # Create a scatter plot of Rating vs Reviews
    fig_rating_vs_reviews = px.scatter(df_filtered, x="Reviews", y="Rating", title="Rating vs Reviews", color="Type", color_discrete_map={"Free": "#5ec962", "Paid": "#fde725"})
    st.plotly_chart(fig_rating_vs_reviews, use_container_width=True)

    # Show DataFrame preview for this plot
    st.subheader("Data Preview for Rating vs Reviews")
    st.write(df_filtered[["App", "Reviews", "Rating"]].head())  # Display top 5 rows of relevant data


# --- USER GUIDE ---
with st.expander("How to Use This Dashboard"):
    st.write("""
    - **Dataset Preview:** Explore the dataset with filters.
    - **Key Insights:** See top-rated and most-reviewed apps.
    - **Analyses:** Navigate to different pages using the sidebar or buttons.
    - **Interactivity:** Use filters and animations to interact with charts.
    """)
