import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Load Data
df = pd.read_csv('google_clean_v2.csv')

# Data Cleaning & Preprocessing
df = df.sort_values(by="Reviews", ascending=False).drop_duplicates(subset=["App"], keep="first")
df = df.sort_index(ascending=True).reset_index(drop=True)
df['Last_Updated'] = pd.to_datetime(df['Last_Updated'])  # Ensure proper datetime format

# Streamlit Sidebar - Metric Selection
metric = st.sidebar.selectbox("Select Metric", options=["Installs", "Reviews"])

# Convert 'App' names to numerical indices for plotting
df['App_Index'] = df['App'].astype('category').cat.codes

# X-axis: Last Updated Date
X = df['Last_Updated']
# Y-axis: App (as numerical index)
Y = df['App_Index']
# Z-axis: Selected metric (Installs or Reviews)
Z = df[metric]

# Reshape Data for Surface Plot
X_unique = np.sort(X.unique())  # Sorted unique timestamps
Y_unique = np.sort(Y.unique())  # Sorted unique app indices

X_grid, Y_grid = np.meshgrid(X_unique, Y_unique)  # Create grid for surface plot

# Create a pivot table for the Z values to fit the X-Y grid
Z_grid = np.full(X_grid.shape, np.nan)

for i, date in enumerate(X_unique):
    for j, app_idx in enumerate(Y_unique):
        values = Z[(X == date) & (Y == app_idx)]
        if not values.empty:
            Z_grid[j, i] = values.mean()  # Assign mean value for stability

# Create 3D Surface Plot
fig = go.Figure()

fig.add_trace(go.Surface(
    x=X_grid,
    y=Y_grid,
    z=Z_grid,
    colorscale='Viridis'
))

# Update Plot Layout
fig.update_layout(
    title=f'3D Surface Plot of {metric} Over Time',
    scene=dict(
        xaxis_title="Date (Last Updated)",
        yaxis_title="App Name (Index)",
        zaxis_title=metric
    ),
    template='plotly_dark'
)

# Display Plot in Streamlit
st.plotly_chart(fig)
