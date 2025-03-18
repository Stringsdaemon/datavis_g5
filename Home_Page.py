import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid


#  wide mode
st.set_page_config(page_title="Gruppe 5 Datenvisualisierung", layout="wide")

#  "logo"

st.sidebar.image("assets/logo_asmodeus.jpg", use_container_width=True)


# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("google_clean_v3.csv")
    df["Last_Updated"] = pd.to_datetime(df["Last_Updated"], errors="coerce", format="%Y-%m-%d")
    return df

df = load_data()

# --- DATASET SUMMARY ---

st.title("Google Play Store Datenvisualisierung")
st.divider()
st.write(
    """
    Dieses Dataset untersucht verschiedene Metriken der vielen Apps, die im Google Play Store angeboten werden, wie die Gesamtzahl 
    der Bewertungen oder Installationen, die Bewertung der App und das Datum der letzten Aktualisierung.
    """
)
st.divider()

# --- PREVIEW METRICS ---
col1, col2, col3, col4 = st.columns(4)

#  CSS FUN!!!ction to display the metric inside a sexy box

def styled_metric(label, value):
    return f"""
    <div style="border: 2px solid #440154; border-radius: 10px; padding: 15px; background-color: #e98eff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
        <h3 style="text-align: center; font-size: 20px; font-weight: bold; color: #440154;">{label}</h3>
        <p style="text-align: center; font-size: 24px; font-weight: bold; color: #440154;">{value}</p>
    </div>
    """

# Display the styled metrics in columns
col1.markdown(styled_metric("Gesamtzahl der Apps", len(df)), unsafe_allow_html=True)
col2.markdown(styled_metric("Durchschnittliche Bewertung", round(df["Rating"].mean(), 2)), unsafe_allow_html=True)
col3.markdown(styled_metric("Häufigste Kategorie", df["Category"].mode()[0]), unsafe_allow_html=True)
col4.markdown(styled_metric("Kostenlos vs Bezahlt", f"{len(df[df['Type'] == 'Free'])} Kostenlos / {len(df[df['Type'] == 'Paid'])} Bezahlt"), unsafe_allow_html=True)

# --- FILTERS ---
st.sidebar.header("Filter Dataset")

# Select specific columns for filtering
selected_type = st.sidebar.selectbox("Typ auswählen", ["Alle"] + df["Type"].unique().tolist())
selected_category = st.sidebar.selectbox("Kategorie auswählen", ["Alle"] + df["Category"].unique().tolist())
selected_rating = st.sidebar.slider("Bewertungsbereich auswählen", min_value=0.0, max_value=5.0, value=(0.0, 5.0))
selected_reviews = st.sidebar.slider("Bewertungen Bereich auswählen", min_value=0, max_value=int(df["Reviews"].max()), value=(0, int(df["Reviews"].max())))

# Apply filters based on user input

df_filtered = df[
    ((df["Type"] == selected_type) | (selected_type == "Alle")) &
    ((df["Category"] == selected_category) | (selected_category == "Alle")) &
    (df["Rating"] >= selected_rating[0]) &
    (df["Rating"] <= selected_rating[1]) &
    (df["Reviews"] >= selected_reviews[0]) &
    (df["Reviews"] <= selected_reviews[1])
]

#  --- data discovery ---

st.subheader("Dataset-Exploration")
# Display the filtered dataframe using AgGrid
AgGrid(df_filtered)

#  ------landing main charts-----

col_main_chart1, col_main_chart2 = st.columns(2)

#  Main Chart 1
with col_main_chart1:
    #  bar chart
    avg_ratings = df_filtered.groupby("Category")["Rating"].mean().sort_values(ascending=False)
    fig_category_ratings = px.bar(avg_ratings, x=avg_ratings.index, y=avg_ratings.values,
                                  title="Durchschnittliche Bewertungen pro Kategorie",
                                  color=avg_ratings.values,
                                  color_continuous_scale="Viridis"
    )
    fig_category_ratings.update_layout(
        yaxis_title="Durchschnittliche Bewertung"
    )
    st.plotly_chart(fig_category_ratings, use_container_width=True)

    #  Show DataFrame preview for this plot
    st.subheader("Datenvorschau für durchschnittliche Bewertungen pro Kategorie")
    st.write(df_filtered.groupby("Category")["Rating"].mean().head())  # Display top 5 rows of the grouped data

# Main Chart 2
with col_main_chart2:
    # Installs x category bar chart
    if "Installs" in df.columns:
        installs_per_category = df_filtered.groupby("Category")["Installs"].sum().sort_values(ascending=False)
        fig_installs = px.bar(installs_per_category, x=installs_per_category.index, y=installs_per_category.values,
                              title="Gesamtinstallationen pro Kategorie",
                              color=avg_ratings.values,
                              color_continuous_scale="Viridis"
        )
        fig_installs.update_layout(
            yaxis_title="Gesamtinstallationen"
        )
        st.plotly_chart(fig_installs, use_container_width=True)

        #  df preview
        st.subheader("Datenvorschau für Installationen pro Kategorie")
        st.write(installs_per_category.head())

# --- secondary charts ---
st.subheader("Schnellanalyse")


col_chart1, col_chart2, col_chart3 = st.columns(3)

#  Chart 1: Distribution of Ratings
with col_chart1:
    # Create a histogram of Ratings Distribution
    fig_hist = px.histogram(df_filtered, x="Rating", nbins=20, title="Verteilung der App-Bewertungen",
                            color_discrete_sequence=["#5ec962"])
    st.plotly_chart(fig_hist, use_container_width=True)

    #  df
    st.subheader("Datenvorschau für Verteilung der Bewertungen")
    st.write(df_filtered[["App", "Rating"]].head())

# Chart 3: Top 10 Most Reviewed Apps
with col_chart2:
    # top 10 reviews preview
    top_reviewed = df_filtered.nlargest(10, "Reviews")
    fig_top_reviews = px.bar(top_reviewed, x="App", y="Reviews", title="Top 10 der am meisten bewerteten Apps",
                             color="Installs", color_continuous_scale="Viridis")
    st.plotly_chart(fig_top_reviews, use_container_width=True)

    # df
    st.subheader("Datenvorschau für Top 10 der am meisten bewerteten Apps")
    st.write(top_reviewed[["App", "Reviews"]].head())

# Chart 3: rating vs reviews
with col_chart3:
    #  Rating vs Reviews scatter
    fig_rating_vs_reviews = px.scatter(df_filtered, x="Reviews", y="Rating", title="Bewertungen vs. Rezensionen", color="Type", color_discrete_map={"Free": "#5ec962", "Paid": "#fde725"})
    st.plotly_chart(fig_rating_vs_reviews, use_container_width=True)

    #  df
    st.subheader("Datenvorschau für Bewertungen vs. Rezensionen")
    st.write(df_filtered[["App", "Reviews", "Rating"]].head())


# --- USER GUIDE ---

with st.expander("Wie man dieses Dashboard verwendet"):
    st.write("""
    - **Dataset-Vorschau:** Erkunden Sie das Dataset mit Filtern.
    - **Wichtige Erkenntnisse:** Sehen Sie sich die am besten bewerteten und meistbewerteten Apps an.
    - **Analysen:** Navigieren Sie zu verschiedenen Seiten über die Seitenleiste oder Schaltflächen.
    - **Interaktivität:** Verwenden Sie Filter und Animationen, um mit Diagrammen zu interagieren.
    """)
