import pandas as pd

def get_top_genres_by_installs(df):
    """Gibt die Top 10 Genres basierend auf Downloads zurück."""
    return df.groupby("Genres")["Installs"].sum().reset_index().sort_values(by="Installs", ascending=False).head(10)
