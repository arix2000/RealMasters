import streamlit as st

from frontend.data.service import get_app_service

loading_messages = [
    "Ładuję manę...",
    "Rzucam na inicjatywę...",
    "Konsultuję się z przedwiecznymi...",
    "Szukam ukrytych pułapek...",
    "Przeszukuję księgi zaklęć...",
    "Karmię smoka...",
    "Ostrzę miecze...",
    "Rzucam K20...",
    "Błagam Mistrza Gry o litość...",
    "Odkrywam mgłę wojny...",
    "Rozbijam obóz...",
    "Przygotowuję mikstury leczące..."
]


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
        st.session_state.type_box_val = "Tworzę postać" if data["action"] == "character_creation" else (
            "Chce się dowiedzieć")
