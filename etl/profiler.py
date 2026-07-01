import pandas as pd
import json
from pathlib import Path
from datetime import datetime


class DataProfiler:

    @staticmethod
    def profile_dataframe(df: pd.DataFrame):
        report = {}

        report["row_count"] = len(df)
        report["column_count"] = len(df.columns)

        report["columns"] = list(df.columns)

        report["memory_usage_kb"] = round(df.memory_usage(deep=True).sum() / 1024, 2)

        # Null values
        report["null_values"] = df.isnull().sum().to_dict()

        # Duplicate rows
        report["duplicate_rows"] = int(df.duplicated().sum())

        # Unique values per column
        report["unique_values"] = {
            col: df[col].nunique()
            for col in df.columns
        }

        return report
    
    
def save_profile_report(report: dict, table_name: str):
    report_dir = Path("reports/profiling")
    report_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report["table"] = table_name
    report["generated_at"] = datetime.now().isoformat()

    output_file = report_dir / f"{table_name}_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    return output_file

    
def profile_csv(file_path: str):
        df = pd.read_csv(file_path)
        return DataProfiler.profile_dataframe(df)