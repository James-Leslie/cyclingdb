"""Data loader for PCM25 rider database."""

import pandas as pd
import requests
import streamlit as st
from pathlib import Path


@st.cache_data
def load_riders_data():
    """Load PCM25 rider data from CSV file or download if not exists.

    Returns:
        pd.DataFrame: DataFrame containing rider data
    """
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    csv_path = data_dir / "riders.csv"

    # Check if CSV exists locally
    if not csv_path.exists():
        st.info("Downloading PCM25 rider database...")
        try:
            download_riders_csv(csv_path)
            st.success("Download complete!")
        except Exception as e:
            st.error(f"Failed to download rider data: {str(e)}")
            st.stop()

    # Load the CSV file
    try:
        # Try UTF-8 first, fallback to Latin-1, use semicolon as delimiter
        try:
            df = pd.read_csv(csv_path, encoding="utf-8", delimiter=";")
        except UnicodeDecodeError:
            df = pd.read_csv(csv_path, encoding="latin-1", delimiter=";")

        # Clean column names (strip whitespace)
        df.columns = df.columns.str.strip()

        # Remove empty columns (like 'Unnamed: 17')
        df = df.dropna(axis=1, how="all")

        # Calculate overall rating as average of stat columns and replace Eval column
        stat_columns = [
            "FL",
            "MO",
            "HL",
            "BA",
            "DH",
            "CS",
            "TT",
            "PR",
            "SP",
            "AC",
            "ST",
            "RS",
            "RC",
        ]
        existing_stat_cols = [col for col in stat_columns if col in df.columns]

        if existing_stat_cols:
            # Convert stat columns to numeric, replacing any non-numeric values with NaN
            for col in existing_stat_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            # Calculate mean, ignoring NaN values
            df["Eval"] = df[existing_stat_cols].mean(axis=1, skipna=True)

            # Round to 1 decimal place for cleaner display
            df["Eval"] = df["Eval"].round(1)

            st.info(
                f"Calculated Eval column from {len(existing_stat_cols)} stat columns. Range: {df['Eval'].min():.1f} - {df['Eval'].max():.1f}"
            )
        else:
            st.warning("No stat columns found for Eval calculation")

        # Basic data validation
        if df.empty:
            st.error("CSV file is empty")
            st.stop()

        # Log basic info
        st.info(f"Loaded {len(df)} riders from database")

        return df

    except Exception as e:
        st.error(f"Failed to load CSV file: {str(e)}")
        st.stop()


def download_riders_csv(csv_path: Path):
    """Download the PCM25 riders CSV from the official source.

    Args:
        csv_path: Path where to save the CSV file
    """
    url = "https://web.cyanide-studio.com/games/cycling/2025/pcm/riders/?export=csv"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # Save to file
        with open(csv_path, "wb") as f:
            f.write(response.content)

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error downloading CSV: {str(e)}")
    except Exception as e:
        raise Exception(f"Error saving CSV file: {str(e)}")


def get_data_stats(df: pd.DataFrame) -> dict:
    """Get basic statistics about the rider data.

    Args:
        df: DataFrame containing rider data

    Returns:
        dict: Dictionary with statistics
    """
    stats = {
        "total_riders": len(df),
        "countries": df["Nationality"].nunique() if "Nationality" in df.columns else 0,
        "teams": df["Team"].nunique() if "Team" in df.columns else 0,
        "columns": list(df.columns),
    }

    return stats


def validate_csv_structure(df: pd.DataFrame) -> bool:
    """Validate that the CSV has expected columns.

    Args:
        df: DataFrame to validate

    Returns:
        bool: True if structure is valid
    """
    expected_columns = ["Name", "Team", "Age"]

    for col in expected_columns:
        if col not in df.columns:
            st.warning(f"Expected column '{col}' not found in CSV")
            return False

    return True
