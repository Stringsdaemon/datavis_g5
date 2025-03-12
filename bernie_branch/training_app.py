import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Fabricating Data (Simplified for Learning)
np.random.seed(42)  # Ensure reproducibility
dates = pd.date_range("2017-01-01", "2021-12-01", freq="MS")  # Monthly data from 2017 to 2021
app_names = [f'App {i+1}' for i in range(10)]  # 10 App names

# Generate synthetic 'Installs' and 'Ratings' for each app over time
data = []
for app in app_names:
    installs = np.random.randint(1000, 10000, size=len(dates))
    ratings = np.random.uniform(3.0, 5.0, size=len(dates))
    for i, date in enumerate(dates):
        data.append([app, date, installs[i], ratings[i]])

# Convert to DataFrame
df = pd.DataFrame(data, columns=['App', 'last_update', 'Installs', 'Rating'])

# Convert 'last_update' to a year-month format
df['last_update'] = df['last_update'].dt.strftime('%Y-%m')

# Sidebar for Metric Selection
metric = st.sidebar.selectbox("Select Metric", options=["Installs", "Rating"])

# Prepare Data for 3D Surface Plot
df['App_Index'] = df['App'].astype('category').cat.codes  # Convert app names to numerical indices
X = pd.to_datetime(df['last_update'])  # Convert 'last_update' to datetime
Y = df['App_Index']  # Numeric representation of App Names
Z = df[metric]  # Metric to visualize

# Create a 3D Surface Plot
fig = go.Figure()

fig.add_trace(go.Surface(
    x=np.tile(X.unique(), (len(app_names), 1)),  # Repeat dates across apps
    y=np.tile(Y.unique().reshape(-1, 1), (1, len(X.unique()))),  # Repeat app indices
    z=Z.values.reshape(len(app_names), -1),  # Reshape Z values to fit grid
    colorscale='Viridis'
))

# Update Layout
fig.update_layout(
    title=f'3D Surface Plot of {metric} Over Time',
    scene=dict(
        xaxis_title="Date (Last Update)",
        yaxis_title="App Name (Index)",
        zaxis_title=metric
    ),
    template='plotly_dark'
)

# Show in Streamlit
st.plotly_chart(fig)
