import streamlit as st
from frontend.global_styles import set_global_styles
import frontend.components as components


def render_page():
    st.set_page_config(layout="wide", page_title="Real Master", initial_sidebar_state="expanded")
    set_global_styles()

    components.history_side_bar()

    _, header_col2, header_col3 = st.columns([1, 1, 1])

    with header_col2:
        with st.container(horizontal_alignment="center"):
            st.image("frontend/assets/dnd_logo.png", width="content")
    with header_col3:
        with st.container(horizontal_alignment="right"):
            st.button("Wyposaż w wiedzę", icon=":material/add:", key="add-files-btn")

    _, main_container, _ = st.columns([1, 20, 1])

    with main_container:
        with st.container(key="main-container"):
            st.image("frontend/assets/real_master.png")

            with st.container(key="chat-container"):
                _, img_col2, _ = st.columns([1, 0.6, 1])
                with img_col2:
                    st.image("frontend/assets/dnd_dice.png", width="stretch")
                    st.header("Ładowanie Many...")

            components.input_fields()
