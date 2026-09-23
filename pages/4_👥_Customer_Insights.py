"""Customer Insights page — interactive segment explorer."""
import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_utils import load_data, kpi_metrics
from src.ui import inject_css, kpi_card, section_header, PRIMARY, ACCENT, SUCCESS, DANGER, WARNING

CHURN_COLOR = {"Yes": "#DC2626", "No": "#16A34A"}
DARK = dict(template="plotly_dark", height=380)


def show_customer_insights():
    inject_css()
    st.markdown("# 👥 Customer Insights")
    st.markdown("Explore customer segments. Adjust the filters to see how KPIs and charts update dynamically.")

    df = load_data()

    with st.sidebar:
        st.markdown("### Segment Filters")
        gender = st.multiselect("Gender", df["gender"].unique(), default=df["gender"].unique())
        contract = st.multiselect("Contract", df["Contract"].unique(), default=df["Contract"].unique())
        inet = st.multiselect("Internet Service", df["InternetService"].unique(), default=df["InternetService"].unique())
        pay = st.multiselect("Payment Method", df["PaymentMethod"].unique(), default=df["PaymentMethod"].unique())
        senior = st.multiselect("Senior Citizen", df["SeniorCitizenLabel"].unique(), default=df["SeniorCitizenLabel"].unique())
        tenure_range = st.slider("Tenure (months)", int(df["tenure"].min()), int(df["tenure"].max()),
                                 (int(df["tenure"].min()), int(df["tenure"].max())))
        monthly_range = st.slider("Monthly Charges ($)", float(df["MonthlyCharges"].min()), float(df["MonthlyCharges"].max()),
                                 (float(df["MonthlyCharges"].min()), float(df["MonthlyCharges"].max())), step=1.0)

    filtered = df[
        df["gender"].isin(gender)
        & df["Contract"].isin(contract)
        & df["InternetService"].isin(inet)
        & df["PaymentMethod"].isin(pay)
        & df["SeniorCitizenLabel"].isin(senior)
        & df["tenure"].between(tenure_range[0], tenure_range[1])
        & df["MonthlyCharges"].between(monthly_range[0], monthly_range[1])
    ]

    if filtered.empty:
        st.warning("No customers match the selected filters. Please widen your selection.")
        return

    m = kpi_metrics(filtered)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi_card("👥", "Selected Customers", f"{m['total']:,}")
    with c2:
        kpi_card("🚪", "Churned", f"{m['churned']:,}")
    with c3:
        kpi_card("📉", "Churn Rate", f"{m['churn_rate']}%")
    with c4:
        kpi_card("💵", "Avg Monthly", f"${m['avg_monthly']}")
    with c5:
        kpi_card("📅", "Avg Tenure", f"{m['avg_tenure']} mo")

    section_header("Segment Visualizations")
    a, b = st.columns(2)
    with a:
        cc = filtered["Churn"].value_counts().reset_index()
        cc.columns = ["Churn", "Count"]
        fig = px.pie(cc, names="Churn", values="Count", title="Churn Distribution (Segment)",
                     color="Churn", color_discrete_map=CHURN_COLOR, hole=0.4)
        fig.update_layout(**DARK)
        st.plotly_chart(fig, use_container_width=True)
    with b:
        g = filtered.groupby("Contract")["Churn"].apply(lambda s: (s == "Yes").mean() * 100).reset_index()
        g.columns = ["Contract", "Churn Rate %"]
        fig = px.bar(g, x="Contract", y="Churn Rate %", color="Contract", title="Churn Rate by Contract (Segment)",
                     color_discrete_sequence=[DANGER, WARNING, SUCCESS])
        fig.update_layout(**DARK, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    c, d = st.columns(2)
    with c:
        fig = px.histogram(filtered, x="tenure", color="Churn", nbins=25, title="Tenure (Segment)",
                           color_discrete_map=CHURN_COLOR)
        fig.update_layout(**DARK, bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
    with d:
        fig = px.box(filtered, x="Churn", y="MonthlyCharges", color="Churn", title="Monthly Charges (Segment)",
                     color_discrete_map=CHURN_COLOR)
        fig.update_layout(**DARK)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.caption(f"Segment contains {m['total']:,} customers out of {len(df):,} total.")


show_customer_insights()
