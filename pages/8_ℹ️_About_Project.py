"""About Project page."""
import streamlit as st
from src.ui import inject_css, section_header, insight_box

TECHS = ["Python", "Pandas", "NumPy", "Scikit-learn", "Plotly", "Matplotlib", "Seaborn", "Streamlit"]
WORKFLOW = [
    "Data Collection", "Data Cleaning", "Exploratory Data Analysis", "Visualization",
    "Feature Engineering", "Machine Learning", "Model Evaluation", "Churn Prediction", "Business Insights",
]


def show_about():
    inject_css()
    st.markdown("# ℹ️ About Project")

    section_header("Project Title")
    st.markdown("**Customer Churn Analysis & Prediction Using AI**")

    section_header("Author")
    st.markdown("**Aryan Kumar**")

    section_header("Program")
    st.markdown("**MCA – Big Data Analytics**")

    section_header("Objective")
    st.markdown("To analyze telecom customer behavior and develop machine-learning models that can identify customers who are likely to churn.")

    section_header("Workflow")
    for i, step in enumerate(WORKFLOW, 1):
        st.markdown(f"**{i}. {step}**" + (" →" if i < len(WORKFLOW) else ""))

    section_header("Technologies Used")
    cols = st.columns(4)
    for i, t in enumerate(TECHS):
        cols[i % 4].markdown(f"- {t}")

    section_header("Models Trained")
    st.markdown("- Logistic Regression\n- Decision Tree Classifier\n- Random Forest Classifier")

    section_header("Dataset")
    st.markdown("IBM Telco Customer Churn dataset — 7,043 customers, 21 attributes including demographics, services, contract details, and churn label.")

    st.markdown("---")
    st.caption("Customer Churn Analysis & Prediction Using AI — Aryan Kumar, MCA Big Data Analytics.")


show_about()
