"""
Data Preprocessing Module for Movie Recommendation System.

This module handles:
1. Loading the movie dataset from CSV.
2. Handling missing values.
3. Cleaning and normalizing text features.
4. Creating a combined feature column for Content-Based Filtering.
"""

from pathlib import Path
import re
import pandas as pd


def get_default_data_path() -> Path:
    """Return the absolute path to the default movies.csv dataset."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / "data" / "movies.csv"


def load_dataset(file_path: str | Path | None = None) -> pd.DataFrame:
    """
    Load movie dataset from a CSV file.

    Parameters:
        file_path (str | Path | None): Path to the CSV file. If None, default path is used.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    if file_path is None:
        file_path = get_default_data_path()
    else:
        file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found at: {file_path}")

    df = pd.read_csv(file_path)
    return df


def clean_text(text: str) -> str:
    """
    Clean text by converting to lowercase, removing punctuation/special characters,
    and removing redundant whitespace.

    Parameters:
        text (str): Input text string.

    Returns:
        str: Cleaned text string.
    """
    if not isinstance(text, str):
        return ""
    # Convert to lowercase
    text = text.lower()
    # Replace non-alphanumeric characters with space
    text = re.sub(r"[^\w\s]", " ", text)
    # Remove multiple spaces and strip ends
    text = re.sub(r"\s+", " ", text).strip()
    return text


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values in critical columns to prevent errors during processing.

    Parameters:
        df (pd.DataFrame): Raw DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame with no NaNs in metadata columns.
    """
    df_clean = df.copy()

    # Required textual columns
    text_columns = ["genres", "overview", "keywords", "cast", "director"]
    for col in text_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna("").astype(str)
        else:
            df_clean[col] = ""

    # Metadata columns
    if "title" in df_clean.columns:
        df_clean["title"] = df_clean["title"].fillna("Unknown Title").astype(str)

    if "rating" in df_clean.columns:
        df_clean["rating"] = pd.to_numeric(df_clean["rating"], errors="coerce").fillna(0.0)

    if "release_year" in df_clean.columns:
        df_clean["release_year"] = pd.to_numeric(df_clean["release_year"], errors="coerce").fillna(0).astype(int)

    if "poster_url" in df_clean.columns:
        df_clean["poster_url"] = df_clean["poster_url"].fillna("")

    return df_clean


def create_combined_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine genres, keywords, overview, cast, and director into a unified feature string.

    Parameters:
        df (pd.DataFrame): Cleaned DataFrame with handled missing values.

    Returns:
        pd.DataFrame: DataFrame containing a new 'combined_features' column.
    """
    df_result = df.copy()

    # Pre-clean each textual field
    cleaned_genres = df_result["genres"].apply(clean_text)
    cleaned_keywords = df_result["keywords"].apply(clean_text)
    cleaned_overview = df_result["overview"].apply(clean_text)
    cleaned_cast = df_result["cast"].apply(clean_text)
    cleaned_director = df_result["director"].apply(clean_text)

    # Combine into a single text representation
    df_result["combined_features"] = (
        cleaned_genres
        + " "
        + cleaned_keywords
        + " "
        + cleaned_overview
        + " "
        + cleaned_cast
        + " "
        + cleaned_director
    )

    # Remove extra spaces
    df_result["combined_features"] = df_result["combined_features"].str.strip()

    return df_result


def preprocess_data(file_path: str | Path | None = None) -> pd.DataFrame:
    """
    Complete pipeline to load, inspect, clean, and engineer features for movies.

    Parameters:
        file_path (str | Path | None): Path to the CSV dataset.

    Returns:
        pd.DataFrame: Preprocessed DataFrame ready for TF-IDF vectorization.
    """
    df_raw = load_dataset(file_path)
    df_filled = handle_missing_values(df_raw)
    df_processed = create_combined_features(df_filled)
    return df_processed


if __name__ == "__main__":
    print("Testing data preprocessing module...")
    processed_df = preprocess_data()
    print(f"Successfully preprocessed {len(processed_df)} movies.")
    print("Sample combined features for first movie:")
    print(processed_df[["title", "combined_features"]].head(2))
