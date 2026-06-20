import streamlit as st

from frontend.data.service import get_app_service
from backend.exceptions import (
    EmptyDocumentError,
    TextProcessingError,
    VectorStoreOperationError,
)

@st.dialog("Dodaj wiedzę", width="large")
def knowledge_upload_dialog():
    uploaded_files = st.file_uploader(
        "Wybierz pliki, które zasilą bazę wiedzy Real Mastera.",
        type=["txt", "md", "csv", "json", "pdf", "docx"],
        accept_multiple_files=True,
        key="knowledge_file_uploader",
        help="Dozwolone formaty: TXT, MD, CSV, JSON, PDF, DOCX",
    )

    if uploaded_files:
        st.write("### Wybrane pliki")
        for file in uploaded_files:
            st.write(f"- {file.name}")

    if st.button(
        "Prześlij",
        key="confirm_knowledge_upload",
        type="primary",
        use_container_width=True,
    ):
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
                    mode="player",
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