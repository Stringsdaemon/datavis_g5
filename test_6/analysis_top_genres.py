import pandas as pd


def get_top_10_genres_by_installs(df):
    """Gibt die 10 beliebtesten App-Genres basierend auf Installationen zurück."""
    df = df.copy()
    df = df.dropna(subset=["Installs", "Genres"])  # Entferne Zeilen ohne Installationszahlen

    # Bereinigung der Installationszahlen
    df["Installs"] = df["Installs"].astype(str).str.replace(r'[^0-9]', '', regex=True).astype(float).astype(int)

    top_genres = df.groupby("Genres")["Installs"].sum().reset_index()
    top_genres = top_genres.sort_values(by="Installs", ascending=False).head(10)  # Sortiere nach Downloads
    return top_genres
