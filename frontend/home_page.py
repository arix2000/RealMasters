import random
import uuid
import streamlit as st
from frontend.global_styles import set_global_styles
import frontend.components as components
import frontend.character_card_component as character_card
from frontend.data.service import get_app_service
from frontend.ui_utils import loading_messages
from backend.exceptions import EmptyDocumentError, TextProcessingError, VectorStoreOperationError


@st.dialog("Dodaj wiedzę", width="large")
def knowledge_upload_dialog():
    st.markdown("### Dodaj wiedzę")
    st.caption("Prześlij pliki, które mają zasilić bazę wiedzy Real Mastera.")

    mode_label = st.radio(
        "Dla kogo dodać wiedzę?",
        options=["Jako gracz", "Jako mistrz gry"],
        horizontal=True,
        key="knowledge_mode_radio"
    )
    selected_mode = "player" if mode_label == "Jako gracz" else "master"

    uploaded_files = st.file_uploader(
        "Prześlij pliki tekstowe",
        type=["txt", "md", "csv", "json", "pdf", "docx"],
        accept_multiple_files=True,
        key="knowledge_file_uploader",
        help="Dozwolone formaty: txt, md, csv, json, pdf, docx"
    )

    if uploaded_files:
        st.write("### Wybrane pliki")
        for file in uploaded_files:
            st.write(f"- {file.name}")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Prześlij", key="confirm-knowledge-upload", type="primary", use_container_width=True):
            if not uploaded_files:
                st.warning("Najpierw dodaj przynajmniej jeden plik.")
                return

            service = get_app_service()
            uploaded_count = 0
            failed_files = []

            for file in uploaded_files:
                try:
                    service.load_file(
                        file=file.getvalue(),
                        filename=file.name,
                        mode=selected_mode
                    )
                    uploaded_count += 1
                except (EmptyDocumentError, TextProcessingError, VectorStoreOperationError) as e:
                    failed_files.append((file.name, str(e)))
                except Exception as e:
                    failed_files.append((file.name, f"Nieoczekiwany błąd: {e}"))

            if uploaded_count > 0:
                st.success(f"Dodano {uploaded_count} plik(ów) do bazy wiedzy.")

            if failed_files:
                st.error("Nie wszystkie pliki udało się przetworzyć:")
                for filename, error_msg in failed_files:
                    st.write(f"- {filename}: {error_msg}")

    with col2:
        st.button("Zamknij", key="close-knowledge-dialog", use_container_width=True)


def render_page():
    st.set_page_config(layout="wide", page_title="Real Master", initial_sidebar_state="expanded")
    set_global_styles()

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "last_character" not in st.session_state:
        st.session_state.last_character = None

    components.history_side_bar()

    _, header_col2, header_col3 = st.columns([1, 1, 1])

    with header_col2:
        with st.container(horizontal_alignment="center"):
            st.image("frontend/assets/dnd_logo.png", width="content")
    with header_col3:
        with st.container(horizontal_alignment="right"):
            if st.button("Wyposaż w wiedzę", icon=":material/add:", key="add-files-btn"):
                knowledge_upload_dialog()

    _, main_container, _ = st.columns([1, 20, 1])

    with main_container:
        with st.container(key="main-container"):
            st.image("frontend/assets/real_master.png")
            render_main_container()

    components.floating_add_button()


def render_main_container():
    chat_container, dice_placeholder = components.render_chat_container()
    service = get_app_service()

    query = components.input_field()
    is_chat_active = len(st.session_state.messages) > 0

    select_col1, select_col2, _ = st.columns([1, 1, 5])
    with select_col1:
        selected_mode = components.selectable_player_box(disabled=is_chat_active)
    with select_col2:
        selected_action = components.selectable_type_box(disabled=is_chat_active)

    if query:
        if len(st.session_state.messages) == 0:
            dice_placeholder.empty()

        st.session_state.messages.append({"role": "user", "content": query})

        selected_message = random.choice(loading_messages)

        with chat_container:
            with st.chat_message("user"):
                st.markdown(query)

            with st.chat_message("assistant"):
                with st.spinner(selected_message):
                    if selected_action == 'asking_question':
                        response = service.submit_chat_prompt(prompt=query, mode=selected_mode)
                        answer_content = response.answer
                    else:
                        response = service.create_character(
                            prompt=query,
                            mode=selected_mode,
                            last_character_response=st.session_state.last_character
                        )
                        st.session_state.last_character = response
                        answer_content = character_card.render(response)

                    st.markdown(answer_content, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": answer_content})

        title = st.session_state.messages[0]["content"][:30]
        is_character = selected_action == 'character_creation'

        service.save_chat_session(
            session_id=st.session_state.session_id,
            title=title,
            is_character=is_character,
            messages=st.session_state.messages,
            last_character=st.session_state.last_character,
            mode=selected_mode,
            action=selected_action
        )

        st.rerun()