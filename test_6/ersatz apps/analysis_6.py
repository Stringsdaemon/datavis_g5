import pandas as pd

def get_top_10_apps(df):
    """Gibt die Top 10 Apps mit den besten Bewertungen zurück."""
    return df.sort_values(by="Rating", ascending=False).head(10)

def get_bottom_10_apps(df):
    """Gibt die Top 10 Apps mit den schlechtesten Bewertungen zurück."""
    return df.sort_values(by="Rating", ascending=True).head(10)

def get_content_rating_distribution(df):
    """Gibt die Anzahl der Apps pro Inhaltsbewertung zurück."""
    return df["Content Rating"].value_counts().reset_index(name="Anzahl").rename(columns={"index": "Content Rating"})

def get_top_genres_by_installs(df):
    """Gibt die Top 10 Genres basierend auf Downloads zurück."""
    return df.groupby("Genres")["Installs"].sum().reset_index().sort_values(by="Installs", ascending=False).head(10)
