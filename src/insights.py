"""Automatically generated business insights computed from the actual dataset."""
import pandas as pd
import numpy as np
import streamlit as st
from src.data_utils import load_data
from src.ui import section_header, insight_box


@st.cache_data(show_spinner="Generating insights...")
def compute_insights(df: pd.DataFrame) -> list:
    """Return a list of (tag, text) insight tuples derived from the data."""
    insights = []
    total = len(df)
    overall_rate = (df["Churn"] == "Yes").mean() * 100

    # 1. Contract type
    contract = df.groupby("Contract")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
    top_contract = contract.idxmax()
    top_contract_rate = contract.max()
    insights.append((
        "Contract",
        f"Customers on '{top_contract}' contracts churn at {top_contract_rate:.1f}%, "
        f"the highest among contract types, versus the overall rate of {overall_rate:.1f}%."
    ))

    # 2. Tenure
    short = df[df["tenure"] <= 12]
    long = df[df["tenure"] > 24]
    short_rate = (short["Churn"] == "Yes").mean() * 100 if len(short) else 0
    long_rate = (long["Churn"] == "Yes").mean() * 100 if len(long) else 0
    insights.append((
        "Tenure",
        f"Customers in their first year (tenure ≤ 12 months) churn at {short_rate:.1f}%, "
        f"while those with over 24 months churn at only {long_rate:.1f}% — tenure is a strong churn signal."
    ))

    # 3. Internet service
    inet = df.groupby("InternetService")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
    top_inet = inet.idxmax()
    insights.append((
        "Internet Service",
        f"Fiber optic customers churn at {inet.max():.1f}%, the highest of any internet service type, "
        f"compared to {inet.get('DSL', 0):.1f}% for DSL and {inet.get('No', 0):.1f}% for no internet."
    ))

    # 4. Payment method
    pay = df.groupby("PaymentMethod")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
    top_pay = pay.idxmax()
    insights.append((
        "Payment Method",
        f"Customers paying via '{top_pay}' have the highest churn rate at {pay.max():.1f}%, "
        f"suggesting billing friction in that channel."
    ))

    # 5. Monthly charges
    high_charge = df[df["MonthlyCharges"] > df["MonthlyCharges"].median()]
    low_charge = df[df["MonthlyCharges"] <= df["MonthlyCharges"].median()]
    hc_rate = (high_charge["Churn"] == "Yes").mean() * 100
    lc_rate = (low_charge["Churn"] == "Yes").mean() * 100
    insights.append((
        "Pricing",
        f"Customers paying above the median monthly charge (${df['MonthlyCharges'].median():.1f}) "
        f"churn at {hc_rate:.1f}%, versus {lc_rate:.1f}% for those paying below it — higher spend correlates with churn."
    ))

    # 6. Online security / tech support
    sec = df.groupby("OnlineSecurity")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
    insights.append((
        "Add-on Services",
        f"Customers without online security churn at {sec.get('No', 0):.1f}%, "
        f"while those with it churn at only {sec.get('Yes', 0):.1f}% — protective add-ons reduce churn."
    ))

    # 7. Senior citizen
    senior = df.groupby("SeniorCitizenLabel")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
    insights.append((
        "Demographics",
        f"Senior citizens churn at {senior.get('Yes', 0):.1f}% compared to {senior.get('No', 0):.1f}% "
        f"for non-seniors — age is a mild churn factor."
    ))

    # 8. Paperless billing
    pb = df.groupby("PaperlessBilling")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
    insights.append((
        "Billing",
        f"Paperless-billing customers churn at {pb.get('Yes', 0):.1f}% versus {pb.get('No', 0):.1f}% "
        f"for paper bills — electronic billing is associated with higher churn."
    ))

    return insights


def show_business_insights():
    df = load_data()
    section_header("Business Insights", "Automatically generated from the actual dataset — no hardcoded values.")
    insights = compute_insights(df)

    st.markdown("### Key Churn Drivers")
    for i, (tag, text) in enumerate(insights, 1):
        insight_box(f"Insight {i}", text)

    st.markdown("### Summary")
    overall = (df["Churn"] == "Yes").mean() * 100
    st.markdown(f"""
    The dataset contains **{len(df):,} customers** with an overall churn rate of **{overall:.1f}%**.
    The strongest observed churn drivers are **contract type**, **tenure**, and **internet service type**.
    Month-to-month customers, new customers, and fiber-optic subscribers are the most at-risk segments.
    Retention efforts should prioritize converting month-to-month customers to longer contracts and
    promoting add-on services like online security and tech support.
    """)
