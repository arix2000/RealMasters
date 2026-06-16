import streamlit as st
from frontend.global_styles import set_global_styles
import frontend.components as components


def render_page():
    st.set_page_config(layout="wide", page_title="Real Master", initial_sidebar_state="expanded")
    set_global_styles()

    components.history_side_bar()

    with st.container(horizontal_alignment="center"):
        st.image("frontend/assets/dnd_logo.png", width="content")

    _, main_container, _ = st.columns([1, 20, 1])

    with main_container:
        with st.container(key="main-container"):
            st.markdown("<span class='main-container-marker'></span>", unsafe_allow_html=True)

            _, _, header_col3 = st.columns([1, 1, 1])
            with header_col3:
                with st.container(horizontal_alignment="right"):
                    st.button("Wyposaż w wiedzę", icon=":material/add:")

            st.image("frontend/assets/real_master.png")

            st.write("\n\n\n")

            _, img_col2, _ = st.columns([1, 0.6, 1], vertical_alignment="center")
            with img_col2:
                st.image("frontend/assets/dnd_dice.png", width="stretch")
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
