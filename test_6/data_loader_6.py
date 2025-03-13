import pandas as pd


def load_data():
    """Lädt die Google Play Store Daten und bereinigt sie."""
    file_path = "google_clean_v2.csv"
    df = pd.read_csv(file_path)

    # Debugging: Überprüfen, ob die Daten geladen wurden
    print("🔍 DataFrame geladen:")
    print(df.head())

    # Sicherstellen, dass alle Werte Strings sind, bevor `.str.replace()` verwendet wird
    if not df["Installs"].dtype == "object":
        df["Installs"] = df["Installs"].astype(str)

    df["Installs"] = pd.to_numeric(df["Installs"].str.replace(',', '').str.replace('+', ''), errors='coerce').fillna(
        0).astype(int)
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors='coerce').fillna(0).astype(int)
    df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce').fillna(0)

    # Debugging: Überprüfen, ob die Bereinigung korrekt war
    print("🔍 Bereinigte Daten Vorschau:")
    print(df.head())

    return df
