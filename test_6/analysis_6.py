import pandas as pd


def get_top_10_apps(df, category):
    """Filtert die Top 10 Apps nach Bewertungen basierend auf der ausgewählten Kategorie."""
    df = df.copy()
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0).astype(int)

    # Filter nach Kategorie
    if category != "Alle Kategorien":
        df = df[df["Category"] == category]

    # Entferne doppelte Apps und nehme nur die höchsten Bewertungen pro App
    top_apps = df.sort_values(by="Reviews", ascending=False).drop_duplicates(subset=["App"]).head(10)
    top_apps = top_apps.sort_values(by="Reviews", ascending=True)  # Sortiere für Animation

    return top_apps


def get_bottom_10_apps(df):
    """Filtert die 10 Apps mit den schlechtesten Bewertungen."""
    df = df.copy()
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0)

    # Entferne Apps ohne Bewertungen
    df = df[df["Rating"] > 0]

    # Sortiere nach Rating aufsteigend und wähle die schlechtesten 10 Apps
    bottom_apps = df.sort_values(by="Rating", ascending=True).head(10)

    return bottom_apps


def get_top_10_genres_by_installs(df):
    """Ermittelt die 10 beliebtesten App-Genres basierend auf Downloads."""
    df = df.copy()
    df["Installs"] = df["Installs"].astype(str).str.replace("[+,]", "", regex=True).astype(float)

    # Gruppiere nach Genre und summiere die Installationen
    genre_installs = df.groupby("Genres")["Installs"].sum().reset_index()

    # Sortiere nach Installationen und wähle die Top 10 Genres
    top_genres = genre_installs.sort_values(by="Installs", ascending=False).head(10)

    return top_genres
