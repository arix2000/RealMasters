import os

from backend.document_processor import DocumentProcessor
from backend.models import ChatResponse, AppMode, CharacterSheet


class RagFacade:
    def __init__(self, api_key: str, vector_dir: str = "data/vectorstore/"):
        player_index_path = os.path.join(vector_dir, "player.index")
        player_chunks_path = os.path.join(vector_dir, "player_chunks.json")

        master_index_path = os.path.join(vector_dir, "master.index")
        master_chunks_path = os.path.join(vector_dir, "master_chunks.json")

        # TODO: Inicjalizacja subkomponentów
        self.document_processor = DocumentProcessor()

    def ingest_context_file(self, file: bytes, filename: str, mode: AppMode) -> None:
        chunks = self.document_processor.process_file(file, filename)


    def process_chat_query(self, query: str, mode: AppMode) -> ChatResponse:
        """
        Generuje odpowiedź raga na zapytanie użytkownika.
        Rzuca:
            GuardrailViolationError: Gdy zapytanie łamie zasady bezpieczeństwa lub jest całkowicie poza tematyką
            MissingContextError: Gdy system nie znajdzie żadnych dopasowań w wektorach i nie ma na czym oprzeć odpowiedzi.
            UpstreamAPIError: Gdy API Google odrzuci request
        """
        pass

    def generate_entity(self, requirements: str, mode: AppMode, entity_to_modify: CharacterSheet = None) -> CharacterSheet:
        """
        Generuje ustrukturyzowany obiekt karty postaci.
        Rzuca:
            GuardrailViolationError: Gdy użytkownik poprosi o wygenerowanie czegoś niezgodnego z tematyką
            StructuredParsingError: Gdy LLM zacznie halucynowac i zwroci niepoprawnego JSON-a
            UpstreamAPIError: Gdy API Google odrzuci request
        """
        pass
