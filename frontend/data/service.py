import streamlit as st

from backend.rag_facade import RagFacade
from backend.models import AppMode, ChatResponse, CharacterSheet


@st.cache_resource
def get_rag_facade() -> RagFacade:
    api_key = st.secrets["API_KEY"]

    return RagFacade(api_key=api_key)


def submit_chat_prompt(prompt: str, mode: AppMode) -> ChatResponse:
    facade = get_rag_facade()
    return facade.process_chat_query(query=prompt, mode=mode)


def load_file(file: bytes, filename: str, mode: AppMode) -> None:
    facade = get_rag_facade()
    facade.ingest_context_file(file=file, filename=filename, mode=mode)


def create_character(prompt: str, mode: AppMode, last_character_response: CharacterSheet = None) -> CharacterSheet:
    facade = get_rag_facade()
    return facade.generate_entity(
        requirements=prompt,
        mode=mode,
        entity_to_modify=last_character_response
    )
