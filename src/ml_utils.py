"""Machine-learning pipeline: preprocessing, training, and prediction."""
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, roc_curve,
)

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
RANDOM_STATE = 42


def build_preprocessor(numeric_features, categorical_features):
    """Build a ColumnTransformer that imputes, scales numerics and one-hots categoricals."""
    numeric_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_features),
            ("cat", categorical_pipe, categorical_features),
        ]
    )


def feature_target_split(df: pd.DataFrame):
    """Separate features and binary target. Churn Yes -> 1, No -> 0."""
    y = (df["Churn"] == "Yes").astype(int)
    X = df.drop(columns=["Churn"])
    # Drop helper label columns that aren't real features
    if "SeniorCitizenLabel" in X.columns:
        X = X.drop(columns=["SeniorCitizenLabel"])
    return X, y


def get_feature_lists(X: pd.DataFrame):
    """Identify numeric vs categorical feature columns from a dataframe."""
    numeric = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical = X.select_dtypes(exclude=[np.number]).columns.tolist()
    return numeric, categorical


@st.cache_resource(show_spinner="Training models...")
def train_models(df: pd.DataFrame):
    """Train Logistic Regression, Decision Tree, and Random Forest.

    Returns a dict with model name -> {pipeline, metrics, y_pred, y_proba, fpr, tpr}.
    """
    X, y = feature_target_split(df)
    numeric, categorical = get_feature_lists(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE, max_depth=6),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
    }

    results = {}
    for name, clf in models.items():
        pipe = Pipeline(steps=[
            ("preprocessor", build_preprocessor(numeric, categorical)),
            ("classifier", clf),
        ])
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_proba = pipe.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        results[name] = {
            "pipeline": pipe,
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "precision": round(precision_score(y_test, y_pred), 4),
            "recall": round(recall_score(y_test, y_pred), 4),
            "f1": round(f1_score(y_test, y_pred), 4),
            "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
            "y_test": y_test,
            "y_pred": y_pred,
            "y_proba": y_proba,
            "fpr": fpr,
            "tpr": tpr,
            "confusion": confusion_matrix(y_test, y_pred),
        }
    return results


def predict_single(pipeline, input_df: pd.DataFrame):
    """Return (label, churn_probability) for a single customer dataframe row."""
    proba = float(pipeline.predict_proba(input_df)[0, 1])
    label = int(proba >= 0.5)
    return label, proba
