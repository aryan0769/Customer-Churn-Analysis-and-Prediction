"""Business Insights page — auto-generated from the dataset."""
import streamlit as st
from src.insights import show_business_insights
from src.ui import inject_css

def show_business_insights_page():
    inject_css()
    show_business_insights()


show_business_insights_page()
