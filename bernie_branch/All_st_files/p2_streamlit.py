#  Price vs rating scatter

import streamlit as st
import pandas as pd
import plotly.express as px

#  Load data:

@st.cache_data
def load_data():
    p2_data = pd.read_csv('google_clean_v2.csv')
    p2_data = p2_data.dropna(subset=['Rating', 'Type', 'Reviews'])
    p2_data['Price']=p2_data['Price'].astype(float)
    return p2_data

p2_data = load_data()

#  Streamlit

st.title('Price vs Rating paradox')
st.write("analyze how ratings differ between free and paid apps")

#  selection filter:

app_type = st.radio('Select price type:', ['All', 'Free', 'Paid'])

#  data filter:

if app_type == 'Free':
    filtered_p2 = p2_data[p2_data['Price'] == 0]
elif app_type == 'Paid':
    filtered_p2 = p2_data[p2_data['Price'] > 0]
else:
    filtered_p2 = p2_data

#  Main plot(Scatter):

fig = px.scatter(
    filtered_p2,
    x= 'Rating',
    y= 'Reviews',
    color= 'Price',
    size= 'Reviews',
    title= f'Rating vs reviews for {app_type} Apps',
    hover_data = ['App']
)
st.plotly_chart(fig)

#  Secondary plot (pie):
#  Filter (Category):

selected_genre = st.selectbox("Select a Genre:", ["All"] + sorted(p2_data["Category"].unique().tolist()))

if selected_genre != "All":
    genre_filtered_p2 = filtered_p2[filtered_p2["Category"] == selected_genre]
else:
    genre_filtered_p2 = filtered_p2

#  Data prep

rating_counts = filtered_p2["Rating"].value_counts().reset_index()
rating_counts.columns = ["Rating", "Count"]

#  plot:

fig_pie = px.pie(
    rating_counts,
    names="Rating",
    values="Count",
    title=f"Ratings Distribution for {app_type} Apps",
    color_discrete_sequence=px.colors.sequential.Viridis
)

st.plotly_chart(fig_pie)


def categorize_rating(rating):
    if rating < 2:
        return "Low (1-2)"
    elif rating < 4:
        return "Medium (3-4)"
    else:
        return "High (4.5-5)"

genre_filtered_p2["Rating Group"] = genre_filtered_p2["Rating"].apply(categorize_rating)

rating_counts = genre_filtered_p2["Rating Group"].value_counts().reset_index()
rating_counts.columns = ["Rating Group", "Count"]

fig_pie = px.pie(
    rating_counts,
    names="Rating Group",
    values="Count",
    title=f"Ratings Distribution ({selected_genre})",
    color_discrete_sequence=px.colors.sequential.Viridis
)

st.plotly_chart(fig_pie)