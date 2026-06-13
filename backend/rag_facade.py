import os

from backend.models import ChatResponse, AppMode, CharacterSheet


class RagFacade:
    def __init__(self, api_key: str, vector_dir: str = "data/vectorstore/"):
        player_index_path = os.path.join(vector_dir, "player.index")
        player_chunks_path = os.path.join(vector_dir, "player_chunks.json")

        master_index_path = os.path.join(vector_dir, "master.index")
        master_chunks_path = os.path.join(vector_dir, "master_chunks.json")
        # TODO: Inicjalizacja subkomponentów
        pass

    def ingest_context_file(self, file: bytes, filename: str, mode: AppMode) -> None:
        """
        Przetwarza plik i ładuje go do bazy wektorowej.
        Rzuca bledy:
            EmptyDocumentError: Gdy plik nie zawiera tekstu lub jest za krótki.
            TextProcessingError: Gdy wystąpi błąd podczas procesowania tekstu
        """
        pass

    def process_chat_query(self, query: str, mode: AppMode) -> ChatResponse:
        """
        Generuje odpowiedź raga na zapytanie użytkownika.
        Rzuca:
            GuardrailViolationError: Gdy zapytanie łamie zasady bezpieczeństwa lub jest całkowicie poza tematyką
            MissingContextError: Gdy system nie znajdzie żadnych dopasowań w wektorach i nie ma na czym oprzeć odpowiedzi.
            UpstreamAPIError: Gdy API Google odrzuci request
        """
        pass

    def generate_entity(self, requirements: str, mode: AppMode) -> CharacterSheet:
        """
        Generuje ustrukturyzowany obiekt karty postaci.
        Rzuca:
            GuardrailViolationError: Gdy użytkownik poprosi o wygenerowanie czegoś niezgodnego z tematyką
            StructuredParsingError: Gdy LLM zacznie halucynowac i zwroci niepoprawnego JSON-a
            UpstreamAPIError: Gdy API Google odrzuci request
        """
        pass
