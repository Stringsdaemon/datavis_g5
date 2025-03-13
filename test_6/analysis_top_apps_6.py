import pandas as pd

def get_top_10_apps(df):
    """Gibt die Top 10 Apps mit den besten Bewertungen zurück."""
    if df.empty:
        print("⚠️ DataFrame ist leer!")
        return pd.DataFrame()
    top_apps = df.sort_values(by="Rating", ascending=False).head(10)
    print("🔍 Top 10 Apps Vorschau:")
    print(top_apps)
    return top_apps

def get_bottom_10_apps(df):
    """Gibt die Top 10 Apps mit den schlechtesten Bewertungen zurück."""
    if df.empty:
        print("⚠️ DataFrame ist leer!")
        return pd.DataFrame()
    bottom_apps = df.sort_values(by="Rating", ascending=True).head(10)
    print("🔍 Bottom 10 Apps Vorschau:")
    print(bottom_apps)
    return bottom_apps
