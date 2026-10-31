from datetime import date
from pathlib import Path
import pandas as pd

REPORTS_DIR = Path(__file__).parent / "reports"


def today_path():
    REPORTS_DIR.mkdir(exist_ok=True)
    return REPORTS_DIR / f"report_{date.today().isoformat()}.xlsx"


def previous_path(current):
    """آخرین فایل قبل از فایل امروز؛ اگر نبود None."""
    files = sorted(REPORTS_DIR.glob("report_*.xlsx"))
    older = [f for f in files if f.name < current.name]
    return older[-1] if older else None


def build_changes(old_df, new_df):
    merged = new_df.merge(
        old_df[["Link", "Price"]],
        on="Link",
        how="outer",
        suffixes=("", "_old"),
        indicator=True,
    )

    def status(row):
        if row["_merge"] == "left_only":
            return "New"
        if row["_merge"] == "right_only":
            return "Removed"
        if pd.isna(row["Price"]) or pd.isna(row["Price_old"]):
            return "Same"
        if row["Price"] > row["Price_old"]:
            return "Up"
        if row["Price"] < row["Price_old"]:
            return "Down"
        return "Same"

    merged["Status"] = merged.apply(status, axis=1)
    merged["Diff"] = merged["Price"] - merged["Price_old"]
    merged["Pct"] = (merged["Diff"] / merged["Price_old"] * 100).round(1)
    changes = merged[(merged["Status"].isin(["New", "Removed"])) | (merged["Pct"].abs() >= 5)]
    cols = ["Name", "Price_old", "Price", "Diff", "Pct", "Status", "Link"]
    return changes[cols].reset_index(drop=True)