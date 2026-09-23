"""Churn Analysis page — 10 interactive charts of churn drivers."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_utils import load_data
from src.ui import inject_css, section_header, insight_box, PRIMARY, ACCENT, SUCCESS, WARNING, DANGER

CHURN_COLOR = {"Yes": "#DC2626", "No": "#16A34A"}
DARK = dict(template="plotly_dark", height=380)


def _churn_rate_by(df, col):
    g = df.groupby(col)["Churn"].apply(lambda s: (s == "Yes").mean() * 100).reset_index()
    g.columns = [col, "Churn Rate %"]
    return g


def show_churn_analysis():
    inject_css()
    st.markdown("# 📈 Churn Analysis")
    st.markdown("Interactive analysis of the key factors that drive customer churn.")

    df = load_data()

    # 1 & 2 — Gender & Senior Citizen
    section_header("Demographics")
    a, b = st.columns(2)
    with a:
        fig = px.bar(_churn_rate_by(df, "gender"), x="gender", y="Churn Rate %", color="gender",
                     title="1. Churn Rate by Gender", color_discrete_sequence=[PRIMARY, ACCENT])
        fig.update_layout(**DARK, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Note", "Churn rates are nearly equal across genders — gender is not a strong churn driver.")

    with b:
        g = _churn_rate_by(df, "SeniorCitizenLabel")
        g["SeniorCitizenLabel"] = g["SeniorCitizenLabel"].map({"Yes": "Senior", "No": "Non-Senior"})
        fig = px.bar(g, x="SeniorCitizenLabel", y="Churn Rate %", color="SeniorCitizenLabel",
                    title="2. Churn Rate by Senior Citizen", color_discrete_sequence=[ACCENT, WARNING])
        fig.update_layout(**DARK, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Note", "Senior citizens show a somewhat higher churn rate than non-seniors.")

    # 3 & 4 — Partner & Dependents
    section_header("Family Status")
    c, d = st.columns(2)
    with c:
        fig = px.bar(_churn_rate_by(df, "Partner"), x="Partner", y="Churn Rate %", color="Partner",
                     title="3. Churn Rate by Partner", color_discrete_sequence=[SUCCESS, DANGER])
        fig.update_layout(**DARK, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Note", "Customers without a partner churn more often than those with one.")
    with d:
        fig = px.bar(_churn_rate_by(df, "Dependents"), x="Dependents", y="Churn Rate %", color="Dependents",
                     title="4. Churn Rate by Dependents", color_discrete_sequence=[SUCCESS, DANGER])
        fig.update_layout(**DARK, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Note", "Customers without dependents have a higher churn rate.")

    # 5 & 6 — Contract & Internet Service
    section_header("Service & Contract")
    e, f = st.columns(2)
    with e:
        fig = px.bar(_churn_rate_by(df, "Contract"), x="Contract", y="Churn Rate %", color="Contract",
                     title="5. Churn Rate by Contract", color_discrete_sequence=[DANGER, WARNING, SUCCESS])
        fig.update_layout(**DARK, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Note", "Month-to-month contracts show a higher churn tendency compared with longer-term contracts.")
    with f:
        fig = px.bar(_churn_rate_by(df, "InternetService"), x="InternetService", y="Churn Rate %", color="InternetService",
                     title="6. Churn Rate by Internet Service", color_discrete_sequence=[PRIMARY, ACCENT, "#64748B"])
        fig.update_layout(**DARK, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        insight_box("Note", "Fiber-optic customers churn at the highest rate among internet service types.")

    # 7 — Payment Method
    section_header("Billing")
    g = _churn_rate_by(df, "PaymentMethod")
    fig = px.bar(g, x="Churn Rate %", y="PaymentMethod", orientation="h", color="PaymentMethod",
                 title="7. Churn Rate by Payment Method", color_discrete_sequence=[PRIMARY, ACCENT, SUCCESS, DANGER])
    fig.update_layout(**DARK, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    insight_box("Note", "Electronic-check payment users churn at the highest rate among payment methods.")

    # 8 — Tenure
    section_header("Tenure & Charges")
    fig = px.histogram(df, x="tenure", color="Churn", nbins=30, marginal="box",
                       title="8. Churn by Tenure", color_discrete_map=CHURN_COLOR)
    fig.update_layout(**DARK, bargap=0.1)
    st.plotly_chart(fig, use_container_width=True)
    insight_box("Note", "Customers with shorter tenure show different churn behavior than long-tenured customers.")

    # 9 — Monthly Charges
    fig = px.box(df, x="Churn", y="MonthlyCharges", color="Churn", color_discrete_map=CHURN_COLOR,
                 title="9. Monthly Charges by Churn")
    fig.update_layout(**DARK)
    st.plotly_chart(fig, use_container_width=True)
    insight_box("Note", "Churned customers tend to have higher monthly charges on average.")

    # 10 — Total Charges
    fig = px.scatter(df, x="tenure", y="TotalCharges", color="Churn", opacity=0.5,
                     title="10. Total Charges vs Tenure by Churn", color_discrete_map=CHURN_COLOR)
    fig.update_layout(**DARK)
    st.plotly_chart(fig, use_container_width=True)
    insight_box("Note", "Total charges scale with tenure; churned customers cluster in the low-tenure region.")

    # Correlation heatmap
    section_header("Numeric Feature Correlation")
    num = df[["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]].copy()
    num["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)
    corr = num.corr()
    fig = px.imshow(corr, text_auto=".2f", title="Correlation Heatmap",
                    color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    fig.update_layout(template="plotly_dark", height=420)
    st.plotly_chart(fig, use_container_width=True)
    insight_box("Note", "Tenure and TotalCharges are strongly positively correlated; ChurnFlag correlates negatively with tenure.")


show_churn_analysis()
