import pandas as pd


def get_content_rating_distribution(df):
    """Gibt die Anzahl der Apps pro Inhaltsbewertung zurück."""
    if df.empty:
        print("⚠️ DataFrame ist leer!")
        return pd.DataFrame()

    content_rating = df["Content Rating"].value_counts().reset_index(name="Anzahl").rename(
        columns={"index": "Content Rating"})

    print("🔍 Inhaltsbewertung Vorschau:")
    print(content_rating)

    return content_rating
