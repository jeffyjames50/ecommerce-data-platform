from pathlib import Path
import pandas as pd


class DataValidator:

    @staticmethod
    def file_exists(file_path: str):
        if not Path(file_path).exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

    @staticmethod
    def read_csv(file_path: str):
        return pd.read_csv(file_path)

    @staticmethod
    def check_empty(df: pd.DataFrame):
        if df.empty:
            raise ValueError("CSV file is empty.")

    @staticmethod
    def check_required_columns(df: pd.DataFrame, required_columns):
        missing = set(required_columns) - set(df.columns)

        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")
        
    @staticmethod
    def check_duplicates(df: pd.DataFrame, key_columns):
        duplicates = df.duplicated(subset=key_columns).sum()

        if duplicates > 0:
            raise ValueError(
                f"Found {duplicates} duplicate rows for keys {key_columns}"
            )
        

    @staticmethod
    def check_nulls(df: pd.DataFrame, required_fields):
        null_counts = df[required_fields].isnull().sum()

        bad_fields = null_counts[null_counts > 0]

        if not bad_fields.empty:
            raise ValueError(
                f"Null values found:\n{bad_fields}"
            )
        

    @staticmethod
    def check_positive_values(df: pd.DataFrame, columns):
        for col in columns:
            if col in df.columns:
                if (df[col] < 0).any():
                    raise ValueError(
                        f"Negative values found in column '{col}'"
                    )