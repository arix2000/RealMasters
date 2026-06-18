from typing import Literal

import streamlit as st

from backend.models import AppMode
from frontend.data.frontend_models import HistoryItem


def history_side_bar():
    st.sidebar.subheader("Ostatnie smoki i lochy:")
    history_items = [
        HistoryItem(entryText="Postać: Gobliński kłamczuch", is_character=True),
        HistoryItem(entryText="Jak pokonać mojego pierwszego smoka", is_character=False),
        HistoryItem(entryText="Postać: Don goblini", is_character=True),
        HistoryItem(entryText="Jaką moc ma czar “dziki wzrok”", is_character=False),
        HistoryItem(entryText="Postać: Gobliński kłamczuch", is_character=True),
        HistoryItem(entryText="Postać: Gobliński kłamczuch", is_character=True),
        HistoryItem(entryText="Jaką moc ma czar “dziki wzrok”", is_character=False),
        HistoryItem(entryText="Jaką moc ma czar “dziki wzrok” Jaką moc ma czar “dziki wzrok” Jaką moc ma czar “dziki "
                              "wzrok”"
                              "moc ma czar “dziki wz", is_character=False)
    ]

    max_text_length = 26

    for i, item in enumerate(history_items):
        if len(item.entryText) > max_text_length:
            display_text = f"{item.entryText[:max_text_length]}..."
        else:
            display_text = item.entryText

        btn_type: Literal["primary", "secondary", "tertiary"] = "primary" if item.is_character else "secondary"

        icon_type = ":material/article_person:" if item.is_character else ":material/history:"

        st.sidebar.button(
            f" {display_text}",
            key=f"history_{i}",
            use_container_width=True,
            icon=icon_type,
            type=btn_type
        )


def input_field():
    return st.chat_input(key="input-field", placeholder="Zapytaj o coś ...")


def selectable_player_box(disabled: bool = False) -> str:
    choice = st.selectbox(
        "Rola",
        ["Jako gracz", "Jako mistrz gry"],
        label_visibility="collapsed",
        disabled=disabled
    )
    return "player" if choice == "Jako gracz" else "master"


def selectable_type_box(disabled: bool = False) -> str:
    return st.selectbox(
        "Akcja",
        ["Tworzę postać", "Chce się dowiedzieć"],
        label_visibility="collapsed",
        disabled=disabled
    )


def render_chat_container():
    chat_container = st.container(key="chat-container")
    dice_placeholder = st.empty()

    with chat_container:
        if len(st.session_state.messages) == 0:
            with dice_placeholder.container():
                _, img_col2, _ = st.columns([1, 0.6, 1])
                with img_col2:
                    st.image("frontend/assets/dnd_dice.png", use_container_width=True)
                    st.header("Zanuć pytanie...", text_alignment="center")
        else:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    return chat_container, dice_placeholder


def floating_add_button():
    if st.button("Nowy chat", icon=":material/add:", key="new_chat_fab"):
        st.session_state.messages = []
        st.rerun()
