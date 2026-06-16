import streamlit as st


def set_global_styles():
    st.markdown("""
    <style>
    
    /* Buttons */
    div[data-testid="stButton"] button[kind="primary"] {
        border-color: #5F0271 !important;
        background-color: transparent !important;
    }
    div[data-testid="stButton"] button {
        border-color: #710246 !important;
        border-radius: 16px !important;
    }
    
    
    /* Container */
    div.st-key-main-container {
        background-color: #202020 !important;
        border: 2px solid #710246 !important;
        border-radius: 42px !important;
        padding: 16px !important;
    }
    
    div.st-key-main-container > div {
        background-color: transparent !important;
    }
    
    
    
    div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
        background-color: #1E1C1C !important;
        border: 1px solid #710246 !important;
        border-radius: 16px !important;
        box-shadow: none !important;
        overflow: hidden !important;
    }
    
    div[data-testid="stTextInput"] input {
        background-color: transparent !important;
        color: #E2E2E2 !important; 
        box-shadow: none !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #1E1C1C !important;
        border: 1px solid #710246 !important;
        border-radius: 16px !important;
        box-shadow: none !important;
        overflow: hidden !important;

    }

    ul[data-baseweb="menu"] {
        background-color: #1E1C1C !important;
        border: 1px solid #710246 !important;
        border-radius: 16px !important;
        overflow: hidden;
    }

    ul[data-baseweb="menu"] li {
        color: #E2E2E2 !important;
    }
    
    div[data-testid="stTextInput"] div[data-baseweb="base-input"]:hover,
    div[data-testid="stSelectbox"] div[data-baseweb="select"]:hover {
        border-color: #5F0271 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)