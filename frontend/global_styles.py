import streamlit as st


def set_global_styles():
    st.markdown("""
    <style>
    div[data-testid="stButton"] button[kind="primary"] {
        border-color: #5F0271 !important;
        background-color: transparent !important;
    }
    div[data-testid="stButton"] button {
        border-color: #710246 !important;
        border-radius: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
