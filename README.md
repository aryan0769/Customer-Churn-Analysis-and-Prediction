# Customer Churn Analysis & Prediction Using AI

**Author:** Aryan Kumar  
**Program:** MCA – Big Data Analytics

An AI-powered analytics dashboard that analyzes telecom customer behavior, identifies churn patterns, and predicts which customers are likely to leave using machine learning.

## Features

- **Dashboard** — KPI cards (total/churned/active customers, churn rate, average charges, tenure) and overview charts
- **Data Overview** — dataset structure, data quality, statistical summary, and an interactive filterable table
- **Churn Analysis** — 10 interactive Plotly charts covering gender, senior citizen, partner, dependents, contract, internet service, payment method, tenure, monthly charges, and total charges, plus a correlation heatmap
- **Customer Insights** — filterable segments (gender, contract, internet, payment, senior, tenure range, monthly charges range) with live-updating KPIs and charts
- **AI Prediction** — enter customer details and get a churn prediction with probability, risk level, and a visual gauge
- **Model Evaluation** — accuracy, precision, recall, F1, ROC-AUC comparison table, ROC curves, and confusion matrices for all three models
- **Business Insights** — automatically generated insights computed from the actual dataset
- **About Project** — objective, workflow, and technologies

## Machine Learning

Three models are trained using a shared preprocessing pipeline (SimpleImputer, OneHotEncoder, StandardScaler via ColumnTransformer):

1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier

Target: `Churn` (Yes = 1, No = 0). Train/test split 80/20 with `random_state=42`.

## Dataset

IBM Telco Customer Churn dataset — 7,043 customers, 21 attributes. Located at `data/Telco-Customer-Churn.csv`.

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501

## Project Structure

```
Aryan_Customer_Churn_AI_Project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── Telco-Customer-Churn.csv
├── models/
├── assets/
├── src/
│   ├── __init__.py
│   ├── data_utils.py
│   ├── ml_utils.py
│   ├── ui.py
│   └── insights.py
└── pages/
    ├── 1_🏠_Dashboard.py
    ├── 2_📊_Data_Overview.py
    ├── 3_📈_Churn_Analysis.py
    ├── 4_👥_Customer_Insights.py
    ├── 5_🤖_AI_Prediction.py
    ├── 6_📋_Model_Evaluation.py
    ├── 7_💡_Business_Insights.py
    └── 8_ℹ️_About_Project.py
```

## Technologies

Python, Pandas, NumPy, Scikit-learn, Plotly, Matplotlib, Seaborn, Streamlit
