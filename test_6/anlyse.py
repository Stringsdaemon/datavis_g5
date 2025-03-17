import pandas as pd

file_path = "google_clean_v2.csv"

try:
    # Load the data assuming it is in the current working directory
    df = pd.read_csv(file_path)
    print("Data successfully loaded.")
except Exception as e:
    print(f"Error loading the data: {e}")
