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
    div.st-key-input-field [data-testid="stChatInput"] * {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important
    }

    div.st-key-input-field [data-testid="stChatInput"] {
        background: #1E1C1C !important;
        background-color: #1E1C1C !important;
        border: 1px solid #710246 !important;
        border-radius: 24px !important;
        padding: 4px 16px !important; 
    }

    div.st-key-input-field [data-testid="stChatInput"]:focus-within {
        border-color: #92035A !important;
    }

    div.st-key-input-field [data-testid="stChatInput"] textarea {
        color: #E2E2E2 !important;
    }

    div.st-key-input-field [data-testid="stChatInput"] button {
        color: #710246 !important;
    }
    
    div.st-key-input-field [data-testid="stChatInput"] button svg {
        fill: #710246 !important;
    }

    div.st-key-input-field [data-testid="stChatInput"] button:hover {
        background: #2C2A2A !important;
        background-color: #2C2A2A !important;
        border-radius: 50% !important;
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