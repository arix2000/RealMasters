import streamlit as st
from frontend.global_styles import set_global_styles
import frontend.components as components


def render_page():
    st.set_page_config(layout="wide", page_title="Real Master", initial_sidebar_state="expanded")
    set_global_styles()

    _, main_container, _ = st.columns([1, 20, 1])

    with main_container:
        with st.container(border=True):
            _, header_col2, header_col3 = st.columns([1, 1, 1])
            with header_col2:
                st.image("frontend/assets/dnd_logo.png", width="content")
            with header_col3:
                st.button("Wyposaż w wiedzę", icon=":material/add:")

            components.history_side_bar()

            st.image("frontend/assets/real_master.png")

            st.write("\n\n\n")

            img_col1, img_col2, img_col3 = st.columns([1, 1, 1], vertical_alignment="center", border=True)
            with img_col2:
                st.image("frontend/assets/dnd_dice.png", width="content")
                st.header("Ładowanie Many...")

            st.write("\n" * 5)

            st.text_input("Twoje pytanie", placeholder="Zapytaj o coś ...", label_visibility="collapsed")

            select_col1, select_col2, select_col3 = st.columns([1, 1, 5])
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
