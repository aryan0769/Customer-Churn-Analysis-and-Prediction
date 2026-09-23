"""Model Evaluation page — metrics table, comparison charts, confusion matrices, ROC curves."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_utils import load_data
from src.ml_utils import train_models
from src.ui import inject_css, section_header, insight_box, PRIMARY, ACCENT, SUCCESS, WARNING, DANGER

DARK = dict(template="plotly_dark", height=400)


def show_model_evaluation():
    inject_css()
    st.markdown("# 📋 Model Evaluation")
    st.markdown("Comparison of three machine-learning models trained on the customer churn dataset.")

    df = load_data()
    results = train_models(df)

    # Metrics table
    section_header("Performance Comparison")
    metrics_df = pd.DataFrame([
        {
            "Model": name,
            "Accuracy": r["accuracy"],
            "Precision": r["precision"],
            "Recall": r["recall"],
            "F1 Score": r["f1"],
            "ROC-AUC": r["roc_auc"],
        }
        for name, r in results.items()
    ])
    st.dataframe(metrics_df.style.highlight_max(axis=0, subset=["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"]),
                 use_container_width=True, hide_index=True)

    # Comparison bar chart
    melted = metrics_df.melt(id_vars="Model", var_name="Metric", value_name="Score")
    fig = px.bar(melted, x="Metric", y="Score", color="Model", barmode="group",
                 title="Model Comparison by Metric", color_discrete_sequence=[PRIMARY, ACCENT, SUCCESS])
    fig.update_layout(**DARK)
    st.plotly_chart(fig, use_container_width=True)

    # ROC curves
    section_header("ROC Curves")
    fig = go.Figure()
    colors = [PRIMARY, ACCENT, SUCCESS]
    for i, (name, r) in enumerate(results.items()):
        fig.add_trace(go.Scatter(x=r["fpr"], y=r["tpr"], mode="lines",
                                 name=f"{name} (AUC={r['roc_auc']})", line=dict(color=colors[i], width=2)))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], line=dict(dash="dash", color="#64748B"),
                             name="Random (AUC=0.5)"))
    fig.update_layout(title="ROC Curve Comparison", xaxis_title="False Positive Rate",
                      yaxis_title="True Positive Rate", **DARK)
    st.plotly_chart(fig, use_container_width=True)

    # Confusion matrices
    section_header("Confusion Matrices")
    cols = st.columns(len(results))
    for i, (name, r) in enumerate(results.items()):
        with cols[i]:
            cm = r["confusion"]
            fig = px.imshow(
                cm, text_auto=True, title=name,
                x=["Pred: Stay", "Pred: Churn"], y=["Actual: Stay", "Actual: Churn"],
                color_continuous_scale="Blues",
            )
            fig.update_layout(template="plotly_dark", height=340)
            st.plotly_chart(fig, use_container_width=True)

    # Best model note (data-driven)
    best = metrics_df.loc[metrics_df["ROC-AUC"].idxmax()]
    insight_box("Best Model (by ROC-AUC)",
                f"{best['Model']} achieves the highest ROC-AUC of {best['ROC-AUC']} among the three models. "
                f"This is the model recommended for churn prediction based on the calculated metrics.")


show_model_evaluation()
