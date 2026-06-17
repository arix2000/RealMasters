import streamlit as st


def set_global_styles():
    st.markdown("""
    <style>
    
    /* Buttons */
    div[data-testid="stButton"] button[kind="primary"] {
        border-color: #5F0271 !important;
        background-color: #1E1C1C !important;
    }
    div[data-testid="stButton"] button {
        border-color: #710246 !important;
        border-radius: 24px !important;
        background-color: #1E1C1C !important;
    }
    
    /* Container */
    div.st-key-main-container {
        background-color: #202020 !important;
        border-radius: 42px !important;
        padding: 24px !important;
    }
    
    div.st-key-main-container > div > div[data-testid="stVerticalBlock"] {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        height: 100% !important;
    }
    
    div.st-key-chat-container {
        flex: 1 1 auto !important;        
        min-height: 50vh !important;
        margin-bottom: 16px !important; 
        padding-right: 8px !important;  
    }

    /* Input Field */
    div[data-testid="stTextArea"] div[data-baseweb="base-input"] {
        background-color: #1E1C1C !important;
        border: 1px solid #710246 !important;
        border-radius: 24px !important;
        box-shadow: none !important;
        height: 84px !important;
        padding: 8px 4px !important;
        overflow: hidden !important;
    }

    /* SelectBoxes */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #1E1C1C !important;
        border: 1px solid #710246 !important;
        border-radius: 24px !important;
        box-shadow: none !important;
        overflow: hidden !important;
    }
    
    </style>
    """, unsafe_allow_html=True)