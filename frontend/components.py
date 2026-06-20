import uuid
import streamlit as st
from typing import Literal

from backend.models import AppMode
from frontend.data.service import get_app_service
from frontend.ui_utils import load_selected_chat

OutputType = Literal['asking_question', 'character_creation']


def history_side_bar():
    st.sidebar.subheader("Ostatnie smoki i lochy:")

    service = get_app_service()
    history_items = service.get_history_list()
    if len(history_items) <= 0:
        st.sidebar.info("Historii jeszcze nie ma ale ty wiesz co zrobić by się zaczęła.")

    max_text_length = 26

    for item in history_items:
        if len(item.entryText) > max_text_length:
            display_text = f"{item.entryText[:max_text_length]}..."
        else:
            display_text = item.entryText

        btn_type: Literal["primary", "secondary", "tertiary"] = "primary" if item.is_character else "secondary"
        icon_type = ":material/article_person:" if item.is_character else ":material/history:"

        st.sidebar.button(
            f" {display_text}",
            width="stretch",
            icon=icon_type,
            type=btn_type,
            key=f"history_{item.session_id}",
            on_click=load_selected_chat,
            args=(item.session_id,)
        )


def floating_add_button():
    if st.button("Nowy chat", icon=":material/add:", key="new_chat_fab"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.last_character = None
        st.rerun()


def selectable_type_box(disabled: bool = False) -> OutputType:
    choice = st.selectbox(
        "Akcja",
        ["Chce się dowiedzieć", "Tworzę postać"],
        key="type_box_val",
        label_visibility="collapsed",
        disabled=disabled
    )
    return 'asking_question' if choice == "Chce się dowiedzieć" else 'character_creation'


def selectable_player_box(disabled: bool = False) -> AppMode:
    choice = st.selectbox(
        "Rola",
        ["Jako gracz", "Jako mistrz gry"],
        key="player_box_val",
        label_visibility="collapsed",
        disabled=disabled
    )
    return "player" if choice == "Jako gracz" else "master"


def input_field():
    return st.chat_input(key="input-field", placeholder="Zapytaj o coś ...")


def render_chat_container():
    chat_container = st.container(key="chat-container")
    dice_placeholder = st.empty()

    with chat_container:
        if len(st.session_state.messages) == 0:
            with dice_placeholder.container():
                _, img_col2, _ = st.columns([1, 0.6, 1])
                with img_col2:
                    st.image("frontend/assets/dnd_dice.png", width="stretch")
                    st.header("Napisz życzenie...", text_alignment="center")
        else:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"], unsafe_allow_html=True)

    return chat_container, dice_placeholder

