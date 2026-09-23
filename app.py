"""
Customer Churn Analysis & Prediction Using AI
=============================================
A Streamlit application that analyzes telecom customer behavior and predicts churn
using Logistic Regression, Decision Tree, and Random Forest models.

Run with:  streamlit run app.py
Opens at:  http://localhost:8501
"""
import streamlit as st
from src.ui import inject_css

# Streamlit's native multipage feature auto-discovers files in the pages/ folder.
# We use the sidebar here only for branding; the page navigation is generated automatically.

st.set_page_config(
    page_title="Customer Churn Analysis & Prediction Using AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

with st.sidebar:
    st.markdown("# 📊 Churn AI")
    st.markdown("**Customer Churn Analysis & Prediction**")
    st.markdown("---")
    st.markdown("Use the navigation above to explore each section.")
    st.markdown("---")
    st.markdown("**Author:** Aryan Kumar")
    st.markdown("**Program:** MCA – Big Data Analytics")
    st.markdown("---")
    st.caption("Powered by Python, Scikit-learn & Streamlit")

# Landing content (the pages/ folder provides the actual pages)
st.markdown("# 📊 Customer Churn Analysis & Prediction Using AI")
st.markdown("### Analyze customer behavior, understand churn patterns, and predict customers who are likely to leave.")
st.markdown("---")
st.markdown(
    "Welcome to the **Customer Churn Analysis & Prediction** dashboard. "
    "Use the sidebar pages to navigate through the application:"
)
st.markdown(
    "- 🏠 **Dashboard** — KPIs and churn overview\n"
    "- 📊 **Data Overview** — dataset structure and quality\n"
    "- 📈 **Churn Analysis** — 10 interactive churn-driver charts\n"
    "- 👥 **Customer Insights** — filterable customer segments\n"
    "- 🤖 **AI Prediction** — predict churn for a new customer\n"
    "- 📋 **Model Evaluation** — model comparison, ROC, confusion matrices\n"
    "- 💡 **Business Insights** — auto-generated insights from the data\n"
    "- ℹ️ **About Project** — project details and workflow"
)
st.markdown("---")
st.success("The application is ready. Select a page from the sidebar to begin.")
