"""Dashboard / Home page — KPIs and overview charts."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_utils import load_data, kpi_metrics
from src.ui import inject_css, kpi_card, section_header, insight_box, PRIMARY, ACCENT, SUCCESS, DANGER, WARNING

CHURN_COLOR = {"Yes": "#DC2626", "No": "#16A34A"}


def show_dashboard():
    inject_css()
    st.markdown("# 🏠 Customer Churn Analysis & Prediction Using AI")
    st.markdown("Analyze customer behavior, understand churn patterns, and predict customers who are likely to leave.")

    df = load_data()
    m = kpi_metrics(df)

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("👥", "Total Customers", f"{m['total']:,}")
    with c2:
        kpi_card("🚪", "Churned Customers", f"{m['churned']:,}", f"{m['churn_rate']}% of base")
    with c3:
        kpi_card("✅", "Active Customers", f"{m['active']:,}")
    with c4:
        kpi_card("📉", "Churn Rate", f"{m['churn_rate']}%")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        kpi_card("💵", "Avg Monthly Charges", f"${m['avg_monthly']}")
    with c6:
        kpi_card("📅", "Avg Tenure", f"{m['avg_tenure']} months")
    with c7:
        kpi_card("🧾", "Contracts", f"{df['Contract'].nunique()} types")
    with c8:
        kpi_card("🌐", "Internet Types", f"{df['InternetService'].nunique()} types")

    st.markdown("---")
    section_header("Project Overview")
    st.markdown(
        "This AI-powered analytics system analyzes telecom customer behavior and uses "
        "machine-learning models to predict customer churn. Explore the dashboard to understand "
        "churn patterns, train models, and predict which customers are likely to leave."
    )

    # Overview charts
    section_header("Churn Distribution & Key Patterns")
    col_a, col_b = st.columns(2)

    with col_a:
        churn_counts = df["Churn"].value_counts().reset_index()
        churn_counts.columns = ["Churn", "Count"]
        fig = px.bar(
            churn_counts, x="Churn", y="Count", color="Churn",
            color_discrete_map=CHURN_COLOR,
            title="Churn Distribution",
            text="Count",
        )
        fig.update_layout(template="plotly_dark", height=360, showlegend=False)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Observation", f"Of {m['total']:,} customers, {m['churned']:,} ({m['churn_rate']}%) have churned.")

    with col_b:
        contract_churn = df.groupby("Contract")["Churn"].apply(lambda s: (s == "Yes").mean() * 100).reset_index()
        contract_churn.columns = ["Contract", "Churn Rate %"]
        fig = px.bar(
            contract_churn, x="Contract", y="Churn Rate %", color="Contract",
            title="Churn Rate by Contract Type",
            color_discrete_sequence=[PRIMARY, ACCENT, WARNING],
        )
        fig.update_layout(template="plotly_dark", height=360, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Observation", "Month-to-month contracts show a higher churn tendency compared with longer-term contracts.")

    col_c, col_d = st.columns(2)
    with col_c:
        fig = px.histogram(
            df, x="tenure", color="Churn", nbins=30, marginal="box",
            title="Customer Tenure Distribution by Churn",
            color_discrete_map=CHURN_COLOR,
        )
        fig.update_layout(template="plotly_dark", height=360, bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Observation", "Customers with shorter tenure churn more frequently than long-tenured customers.")

    with col_d:
        pay_churn = df.groupby("PaymentMethod")["Churn"].apply(lambda s: (s == "Yes").mean() * 100).reset_index()
        pay_churn.columns = ["Payment Method", "Churn Rate %"]
        fig = px.bar(
            pay_churn, x="Churn Rate %", y="Payment Method", orientation="h", color="Payment Method",
            title="Churn Rate by Payment Method",
            color_discrete_sequence=[PRIMARY, ACCENT, SUCCESS, DANGER],
        )
        fig.update_layout(template="plotly_dark", height=360, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Observation", "Electronic-check payment users churn at the highest rate among payment methods.")


show_dashboard()
