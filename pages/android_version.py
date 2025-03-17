import pandas as pd
import streamlit as st
import plotly.express as px
import time


# Load your data
data = pd.read_csv('google_clean_v3.csv')

# Group by Android Version and calculate average installs
android_version_installs = data.groupby('Android Ver')['Installs'].mean().reset_index()

# Streamlit app
st.title('Interactive and Animated Visualization')

# Animation speed slider
speed = st.slider("Animationsgeschwindigkeit", 0.05, 1.0, 0.2, 0.05)

# Year selection slider
years = sorted(data['year_last_update'].unique())
selected_year = st.slider("Select Year", min_value=min(years), max_value=max(years), value=min(years))

# Checkbox for Android version selection
android_versions = sorted(data['Android Ver'].unique())
selected_android_versions = st.multiselect("Select Android Versions", android_versions, default=android_versions)

# Filter data based on selected year and Android versions
filtered_data = data[
    (data['year_last_update'] == selected_year) & (data['Android Ver'].isin(selected_android_versions))]
android_version_installs_filtered = filtered_data.groupby('Android Ver')['Installs'].mean().reset_index()

# Plot line chart for average installs by Android version with interactivity
fig_android_version_installs = px.line(android_version_installs_filtered, x='Android Ver', y='Installs',
                                       title=f'Average Installs by Android Version in {selected_year}',
                                       labels={'Android Ver': 'Android Version', 'Installs': 'Average Installs'},
                                       template='plotly_dark')

# Add hover tooltips
fig_android_version_installs.update_traces(mode='markers+lines',
                                           hovertemplate='Android Version: %{x}<br>Installs: %{y}')

# Add zoom and pan functionality (enabled by default in Plotly)
fig_android_version_installs.update_layout(
    xaxis=dict(rangeslider=dict(visible=True)),
    yaxis=dict(fixedrange=False)
)

# Display the Plotly figure in Streamlit
chart = st.plotly_chart(fig_android_version_installs, use_container_width=True, key='initial_chart')

# Animation control
if st.button("▶️ Play Animation"):
    for year in years:
        filtered_data = data[(data['year_last_update'] == year) & (data['Android Ver'].isin(selected_android_versions))]
        android_version_installs_filtered = filtered_data.groupby('Android Ver')['Installs'].mean().reset_index()

        fig_android_version_installs = px.line(android_version_installs_filtered, x='Android Ver', y='Installs',
                                               title=f'Average Installs by Android Version in {year}',
                                               labels={'Android Ver': 'Android Version',
                                                       'Installs': 'Average Installs'},
                                               template='plotly_dark')

        fig_android_version_installs.update_traces(mode='markers+lines',
                                                   hovertemplate='Android Version: %{x}<br>Installs: %{y}')
        fig_android_version_installs.update_layout(
            xaxis=dict(rangeslider=dict(visible=True)),
            yaxis=dict(fixedrange=False)
        )

        chart.plotly_chart(fig_android_version_installs, use_container_width=True, key=f'chart_{year}')
        time.sleep(speed)