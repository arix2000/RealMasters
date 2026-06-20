import json
import os

import streamlit as st

from backend.models import AppMode, ChatResponse, CharacterSheet
from backend.rag_facade import RagFacade
from frontend.data.frontend_models import HistoryItem


class AppService:
    def __init__(self, api_key: str):
        self.facade = RagFacade(api_key=api_key)
        self.history_dir = "chat_history"

        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

    def submit_chat_prompt(self, prompt: str, mode: AppMode, chat_history: list = None) -> ChatResponse:
        return self.facade.process_chat_query(query=prompt, mode=mode, chat_history=chat_history)

    def load_file(self, file: bytes, filename: str, mode: AppMode) -> None:
        self.facade.ingest_context_file(file=file, filename=filename, mode=mode)

    def create_character(self, prompt: str, mode: AppMode,
                         last_character_response: CharacterSheet = None) -> CharacterSheet:
        return self.facade.generate_entity(
            requirements=prompt,
            mode=mode,
            entity_to_modify=last_character_response
        )

    def save_chat_session(self, session_id: str, title: str, is_character: bool, messages: list, last_character: CharacterSheet | None, mode: str, action: str):
        filepath = os.path.join(self.history_dir, f"{session_id}.json")

        data = {
            "session_id": session_id,
            "title": title,
            "is_character": is_character,
            "mode": mode,
            "action": action,
            "messages": messages,
            "last_character": last_character.model_dump() if last_character else None
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save session {session_id}. Error: {e}")

    def get_history_list(self) -> list[HistoryItem]:
        histories = []

        if not os.path.exists(self.history_dir):
            return histories

        for filename in sorted(os.listdir(self.history_dir), reverse=True):
            filepath = os.path.join(self.history_dir, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    histories.append(HistoryItem(
                        session_id=data["session_id"],
                        entryText=data["title"],
                        is_character=data["is_character"]
                    ))
                except Exception:
                    print(f"history file open failed, data: " + data)
                    continue

        return histories

    def load_chat_session(self, session_id: str) -> dict:
        filepath = os.path.join(self.history_dir, f"{session_id}.json")

        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                if data.get("last_character"):
                    data["last_character"] = CharacterSheet.model_validate(data["last_character"])
                return data

        return {}


@st.cache_resource
def get_app_service() -> AppService:
    api_key = st.secrets["API_KEY"]
    return AppService(api_key=api_key)
