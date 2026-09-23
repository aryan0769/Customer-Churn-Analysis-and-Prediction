"""AI Prediction page — form, prediction, and risk visualization."""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.data_utils import load_data
from src.ml_utils import train_models, predict_single
from src.ui import inject_css, kpi_card, section_header, insight_box, PRIMARY, SUCCESS, WARNING, DANGER


def show_prediction():
    inject_css()
    st.markdown("# 🤖 AI Churn Prediction")
    st.markdown("Enter a customer's details below to predict whether they are likely to churn.")

    df = load_data()
    results = train_models(df)

    # Let user pick which model to use
    model_name = st.selectbox("Select Model", list(results.keys()), index=0)
    pipeline = results[model_name]["pipeline"]

    st.markdown("---")
    section_header("Customer Information")

    c1, c2, c3 = st.columns(3)
    with c1:
        gender = st.selectbox("Gender", df["gender"].unique())
        senior = st.selectbox("Senior Citizen", ["Yes", "No"])
        partner = st.selectbox("Partner", df["Partner"].unique())
        dependents = st.selectbox("Dependents", df["Dependents"].unique())
        tenure = st.slider("Tenure (months)", 0, 72, 12)
        phone = st.selectbox("Phone Service", df["PhoneService"].unique())
    with c2:
        multiple = st.selectbox("Multiple Lines", df["MultipleLines"].unique())
        inet = st.selectbox("Internet Service", df["InternetService"].unique())
        online_sec = st.selectbox("Online Security", df["OnlineSecurity"].unique())
        online_backup = st.selectbox("Online Backup", df["OnlineBackup"].unique())
        device_prot = st.selectbox("Device Protection", df["DeviceProtection"].unique())
        tech_support = st.selectbox("Tech Support", df["TechSupport"].unique())
    with c3:
        streaming_tv = st.selectbox("Streaming TV", df["StreamingTV"].unique())
        streaming_movies = st.selectbox("Streaming Movies", df["StreamingMovies"].unique())
        contract = st.selectbox("Contract", df["Contract"].unique())
        paperless = st.selectbox("Paperless Billing", df["PaperlessBilling"].unique())
        payment = st.selectbox("Payment Method", df["PaymentMethod"].unique())
        monthly = st.number_input("Monthly Charges ($)", 0.0, 200.0, 50.0, step=1.0)
        total = st.number_input("Total Charges ($)", 0.0, 10000.0, 1000.0, step=50.0)

    # Build input dataframe matching training feature columns
    input_dict = {
        "gender": gender,
        "SeniorCitizen": 1 if senior == "Yes" else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": inet,
        "OnlineSecurity": online_sec,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_prot,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total,
    }
    input_df = pd.DataFrame([input_dict])

    if st.button("Predict Churn", type="primary"):
        try:
            label, proba = predict_single(pipeline, input_df)
            pct = proba * 100

            if pct < 40:
                risk = "Low Risk"
                risk_color = SUCCESS
            elif pct < 70:
                risk = "Medium Risk"
                risk_color = WARNING
            else:
                risk = "High Risk"
                risk_color = DANGER

            outcome = "Likely to Churn" if label == 1 else "Likely to Stay"

            section_header("Prediction Result")

            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown(f"""
                <div class="risk-card">
                    <div class="risk-label" style="color:{risk_color};">{outcome}</div>
                    <div style="color:#94A3B8; margin-top:8px;">{risk}</div>
                </div>
                """, unsafe_allow_html=True)
            with r2:
                st.markdown(f"""
                <div class="risk-card">
                    <div class="risk-prob" style="color:{risk_color};">{pct:.1f}%</div>
                    <div style="color:#94A3B8;">Churn Probability</div>
                </div>
                """, unsafe_allow_html=True)
            with r3:
                st.markdown(f"""
                <div class="risk-card">
                    <div class="risk-label" style="color:#60A5FA;">{model_name}</div>
                    <div style="color:#94A3B8; margin-top:8px;">Model Used</div>
                </div>
                """, unsafe_allow_html=True)

            # Risk gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pct,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Churn Probability", "font": {"color": "#F1F5F9"}},
                number={"suffix": "%", "font": {"color": risk_color}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
                    "bar": {"color": risk_color},
                    "steps": [
                        {"range": [0, 40], "color": "#1E3A2F"},
                        {"range": [40, 70], "color": "#3A2E1A"},
                        {"range": [70, 100], "color": "#3A1A1A"},
                    ],
                    "threshold": {
                        "line": {"color": "#F1F5F9", "width": 3},
                        "thickness": 0.85, "value": pct,
                    },
                },
            ))
            fig.update_layout(template="plotly_dark", height=260)
            st.plotly_chart(fig, use_container_width=True)

            insight_box(
                "Explanation",
                f"Based on the entered customer information, the {model_name} model estimates "
                f"a churn probability of {pct:.1f}%. This is classified as {risk}."
            )
            st.caption("This prediction reflects the model's estimate from the entered inputs. It does not explain causation.")
        except Exception as e:
            st.error(f"Prediction failed: {e}")


show_prediction()
