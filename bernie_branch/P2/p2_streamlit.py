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

app_type = st.radio('Select price type:', ['Free', 'Paid'])

#  data filter:

if app_type == 'Free':
    filtered_p2 = p2_data[p2_data['Price'] == 0]
else:
    filtered_p2 = p2_data[p2_data['Price'] > 0]

#  plot:

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