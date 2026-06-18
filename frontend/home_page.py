import streamlit as st
from frontend.global_styles import set_global_styles
import frontend.components as components
from frontend.data.service import submit_chat_prompt


def render_page():
    st.set_page_config(layout="wide", page_title="Real Master", initial_sidebar_state="expanded")
    set_global_styles()

    if "messages" not in st.session_state:
        st.session_state.messages = []

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
            render_main_container()


def render_main_container():
    chat_container, dice_placeholder = components.render_chat_container()

    query = components.input_field()

    select_col1, select_col2, _ = st.columns([1, 1, 5])
    with select_col1:
        selected_mode = components.selectable_player_box()
    with select_col2:
        selected_action = components.selectable_type_box()

    if query:
        if len(st.session_state.messages) == 0:
            dice_placeholder.empty()

        st.session_state.messages.append({"role": "user", "content": query})

        with chat_container:
            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                with st.spinner("Ładuje mane..."):
                    response = submit_chat_prompt(prompt=query, mode=selected_mode)
                    st.markdown(response.answer)

        st.session_state.messages.append({"role": "assistant", "content": response.answer})

        st.rerun()
