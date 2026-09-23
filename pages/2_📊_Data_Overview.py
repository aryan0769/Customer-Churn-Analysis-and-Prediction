"""Data Overview page — structure, quality, and interactive table."""
import pandas as pd
import streamlit as st

from src.data_utils import load_data, data_summary
from src.ui import inject_css, kpi_card, section_header, PRIMARY, ACCENT, SUCCESS, WARNING, DANGER


def show_data_overview():
    inject_css()
    st.markdown("# 📊 Data Overview")
    st.markdown("Inspect the structure, quality, and contents of the customer churn dataset.")

    df = load_data()
    info = data_summary(df)

    # Top KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("📐", "Rows", f"{info['rows']:,}")
    with c2:
        kpi_card("📏", "Columns", f"{info['cols']}")
    with c3:
        kpi_card("🔁", "Duplicates", f"{info['duplicates']}")
    with c4:
        total_missing = sum(info["missing"].values())
        kpi_card("❓", "Missing Values", f"{total_missing}", "filled after cleaning")

    # Column structure
    section_header("Dataset Structure")
    struct = pd.DataFrame({
        "Column": info["column_names"],
        "Data Type": [info["dtypes"][c] for c in info["column_names"]],
        "Missing Values": [info["missing"].get(c, 0) for c in info["column_names"]],
    })
    st.dataframe(struct, use_container_width=True, hide_index=True)

    # Data quality
    section_header("Data Quality")
    qc1, qc2 = st.columns(2)
    with qc1:
        st.markdown("**Numeric Columns**")
        st.write(info["numeric_cols"])
        st.markdown("**Categorical Columns**")
        st.write(info["categorical_cols"])
    with qc2:
        st.markdown("**Missing Values Handling**")
        st.info(
            "TotalCharges had 11 blank entries (customers with tenure = 0, i.e. brand-new). "
            "These were converted to numeric and filled with 0. No rows were deleted. "
            "No duplicate rows were found."
        )

    # Statistical summary
    section_header("Statistical Summary")
    st.dataframe(df.describe(include="all").T, use_container_width=True)

    # Interactive table with filter
    section_header("Dataset Preview")
    st.markdown("Filter and browse the full dataset below.")
    show_cols = [c for c in df.columns if c != "SeniorCitizenLabel"]
    df_view = df[show_cols]

    with st.expander("Filters", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            churn_filter = st.multiselect("Churn", df["Churn"].unique(), default=df["Churn"].unique())
        with fc2:
            contract_filter = st.multiselect("Contract", df["Contract"].unique(), default=df["Contract"].unique())
        with fc3:
            inet_filter = st.multiselect("Internet Service", df["InternetService"].unique(), default=df["InternetService"].unique())

    filtered = df_view[
        df_view["Churn"].isin(churn_filter)
        & df_view["Contract"].isin(contract_filter)
        & df_view["InternetService"].isin(inet_filter)
    ]
    st.dataframe(filtered, use_container_width=True, height=450)
    st.caption(f"Showing {len(filtered):,} of {len(df):,} rows")


show_data_overview()
