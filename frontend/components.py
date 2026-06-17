from typing import Literal

import streamlit as st

from frontend.history_entry import HistoryItem


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


def input_fields():
    st.text_area("", placeholder="Zapytaj o coś ...", label_visibility="collapsed")

    select_col1, select_col2, _ = st.columns([1, 1, 5])
    with select_col1:
        st.selectbox(
            "Rola",
            ["Jako gracz", "Jako mistrz gry"],
            label_visibility="collapsed"
        )
    with select_col2:
        st.selectbox(
            "Akcja",
            ["Tworzę postać", "Chce się dowiedzieć"],
            label_visibility="collapsed"
        )
