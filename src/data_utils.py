"""Data loading and cleaning utilities for the Customer Churn project."""
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Telco-Customer-Churn.csv"


@st.cache_data(show_spinner="Loading dataset...")
def load_data() -> pd.DataFrame:
    """Load the Telco Customer Churn dataset and clean it for analysis."""
    if not DATA_PATH.exists():
        st.error(f"Dataset not found at {DATA_PATH}. Please place Telco-Customer-Churn.csv in the data/ folder.")
        st.stop()

    raw = pd.read_csv(DATA_PATH)

    # Standardize column names (keep original for display, but ensure no stray spaces)
    raw.columns = [c.strip() for c in raw.columns]

    # TotalCharges comes in as a string with empty values for brand-new customers
    raw["TotalCharges"] = pd.to_numeric(raw["TotalCharges"], errors="coerce")
    # The 11 rows with NaN TotalCharges all have tenure=0 (just joined). Fill with 0.
    raw["TotalCharges"] = raw["TotalCharges"].fillna(0.0)

    # SeniorCitizen is 0/1 -> make a readable version for charts
    raw["SeniorCitizenLabel"] = raw["SeniorCitizen"].map({0: "No", 1: "Yes"})

    # Drop customerID for analysis but keep a copy for display if needed
    if "customerID" in raw.columns:
        raw = raw.drop(columns=["customerID"])

    return raw


@st.cache_data(show_spinner="Computing summary...")
def data_summary(df: pd.DataFrame) -> dict:
    """Return a dictionary of data-quality metrics for the Data Overview page."""
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),  # rows may duplicate after dropping customerID; this is expected
        "numeric_cols": df.select_dtypes(include=[np.number]).columns.tolist(),
        "categorical_cols": df.select_dtypes(exclude=[np.number]).columns.tolist(),
    }


def kpi_metrics(df: pd.DataFrame) -> dict:
    """Compute the headline KPIs shown on the dashboard."""
    total = len(df)
    churned = int((df["Churn"] == "Yes").sum())
    active = total - churned
    churn_rate = round(churned / total * 100, 2) if total else 0.0
    avg_monthly = round(df["MonthlyCharges"].mean(), 2) if total else 0.0
    avg_tenure = round(df["tenure"].mean(), 1) if total else 0.0
    return {
        "total": total,
        "churned": churned,
        "active": active,
        "churn_rate": churn_rate,
        "avg_monthly": avg_monthly,
        "avg_tenure": avg_tenure,
    }
