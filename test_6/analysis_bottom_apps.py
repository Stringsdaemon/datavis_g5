import pandas as pd

def get_bottom_10_apps_by_rating(df):
    """Gibt die 10 Apps mit den niedrigsten Bewertungen zurück."""
    df = df.copy()
    df = df.dropna(subset=["Rating"])  # Entferne Zeilen ohne Bewertung
    df = df.sort_values(by="Rating", ascending=True).head(10)  # Sortiere nach Bewertung aufsteigend
    return df
