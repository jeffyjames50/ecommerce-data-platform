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