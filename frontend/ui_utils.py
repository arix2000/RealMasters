import streamlit as st

from frontend.data.service import get_app_service


def load_selected_chat(session_id: str):
    service = get_app_service()
    data = service.load_chat_session(session_id)
    if data:
        st.session_state.session_id = data["session_id"]
        st.session_state.messages = data["messages"]
        st.session_state.last_character = data["last_character"]

    if "mode" in data:
        st.session_state.player_box_val = "Jako mistrz gry" if data["mode"] == "master" else "Jako gracz"
    if "action" in data:
        st.session_state.type_box_val = "Tworzę postać" if data["action"] == "character_creation" else ("Chce się dowiedzieć")