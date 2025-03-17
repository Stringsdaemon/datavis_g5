import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import numpy as np
import os

# Daten laden mit Fehlerhandling
def load_data():
    file_path = "google_clean_v2.csv"
    try:
        df = pd.read_csv(file_path)
        df["Price"] = pd.to_numeric(df["Price"].astype(str).str.replace("$", ""), errors="coerce")
        df["Installs"] = pd.to_numeric(df["Installs"].astype(str).str.replace(",", "").str.replace("+", ""), errors="coerce")
    except Exception as e:
        st.error(f"Fehler beim Lesen der Daten: {e}")
