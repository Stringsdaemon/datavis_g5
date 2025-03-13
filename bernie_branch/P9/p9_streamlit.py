import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


# Cache data processing steps
@st.cache_data
def load_and_process_data():
    # Load data
    df = pd.read_csv('google_clean_v2.csv')

    # Handle missing values
    df = df.dropna(subset=['Genres', 'Installs', 'Last_Updated'])

    # Split combined genres and explode dataframe
    df['Genres'] = df['Genres'].str.split(';')
    df = df.explode('Genres')
    df['Genres'] = df['Genres'].str.strip()

    # Convert installs to numeric
    #df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
    df = df.dropna(subset=['Installs'])

    # Parse dates and create period column
    df['Last_Updated'] = pd.to_datetime(df['Last_Updated'], errors='coerce')
    df = df.dropna(subset=['Last_Updated'])
    df['Period'] = df['Last_Updated'].dt.to_period('M').dt.to_timestamp()

    # Aggregate data
    genre_time = df.groupby(['Genres', 'Period'])['Installs'].sum().reset_index()

    # Calculate cumulative installs and ranking
    genre_time = genre_time.sort_values('Period')
    genre_time['Cumulative_Installs'] = genre_time.groupby('Genres')['Installs'].cumsum()
    genre_time['Rank'] = genre_time.groupby('Period')['Cumulative_Installs'].rank(ascending=False, method='first')

    return genre_time


# Load processed data
genre_time = load_and_process_data()

# Streamlit UI
st.title('Genre Popularity Race')
st.markdown("""
**Note:** Popularity is calculated based on cumulative installs of apps grouped by their last update date.
App updates may not reflect actual release dates.
""")

# Widgets
min_date = genre_time['Period'].min().date()
max_date = genre_time['Period'].max().date()
selected_n = st.slider('Number of Top Genres', 5, 25, 10)
date_range = st.slider('Date Range',
                       min_value=min_date,
                       max_value=max_date,
                       value=(min_date, max_date))

# Filter data
filtered_data = genre_time[
    (genre_time['Period'].dt.date >= date_range[0]) &
    (genre_time['Period'].dt.date <= date_range[1]) &
    (genre_time['Rank'] <= selected_n)
    ]

# Create visualization
fig = px.bar(filtered_data.sort_values(['Period', 'Rank']),
             x='Cumulative_Installs',
             y='Genres',
             animation_frame='Period',
             orientation='h',
             color='Genres',
             text='Cumulative_Installs',
             range_x=[0, filtered_data['Cumulative_Installs'].max() * 1.1],
             height=600)

# Format animation
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 100
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 50
fig.update_layout(showlegend=False,
                  xaxis_title='Total Installs',
                  yaxis_title='Genre',
                  yaxis={'categoryorder': 'total ascending'})

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Performance tips section
st.markdown("""
**Performance Optimization Tips:**
1. Use monthly periods instead of daily
2. Limit date range using the slider
3. Reduce number of displayed genres
4. Prefer Chrome over other browsers for animation
""")

# Troubleshooting section
st.markdown("""
**Common Issues:**
- Missing genres: Ensure original data has complete genre info
- Choppy animation: Reduce date range or number of genres
- Empty plot: Check date range selection includes valid data
- Encoding errors: Verify CSV encoding (try utf-8 or latin-1)
""")