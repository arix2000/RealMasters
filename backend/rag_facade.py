import os

from backend.document_processor import DocumentProcessor
from backend.llm_client import LLMClient
from backend.models import ChatResponse, AppMode, CharacterSheet, SourceDocument
from backend.prompt_and_guardrail_manager import PromptAndGuardrailManager
from backend.vector_manager import VectorStoreManager


class RagFacade:
    def __init__(self, api_key: str, vector_dir: str = "data/vectorstore/"):
        player_index_path = os.path.join(vector_dir, "player.index")
        player_chunks_path = os.path.join(vector_dir, "player_chunks.json")

        master_index_path = os.path.join(vector_dir, "master.index")
        master_chunks_path = os.path.join(vector_dir, "master_chunks.json")

        self.document_processor = DocumentProcessor()
        self.prompt_manager = PromptAndGuardrailManager()
        self.llm_client = LLMClient(api_key=api_key)
        self.vector_manager = VectorStoreManager()

        self.vector_manager.load_store('player', player_index_path, player_chunks_path)
        self.vector_manager.load_store('master', master_index_path, master_chunks_path)

    def ingest_context_file(self, file: bytes, filename: str, mode: AppMode) -> None:
        chunks = self.document_processor.process_file(file, filename)

        self.vector_manager.add_custom_context(chunks, mode)


    def process_chat_query(self, query: str, mode: AppMode) -> ChatResponse:
        self.prompt_manager.check_guardrails(query)

        retrieved_docs = self.vector_manager.search_similar(query, mode, k=3)

        context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])

        final_prompt = self.prompt_manager.build_chat_prompt(
            query=query,
            context=context_text,
            mode=mode
        )

        answer_text = self.llm_client.generate_chat_response(final_prompt)

        sources = [
            SourceDocument(content=doc.page_content, metadata=doc.metadata)
            for doc in retrieved_docs
        ]

        return ChatResponse(
            answer=answer_text,
            sources=sources,
            is_guardrail_triggered=False
        )

    def generate_entity(self, requirements: str, mode: AppMode, entity_to_modify: CharacterSheet = None) -> CharacterSheet:
        self.prompt_manager.check_guardrails(requirements)

        is_modification = entity_to_modify is not None

        if is_modification:
            current_state_json = entity_to_modify.model_dump_json()
            requirements = f"Current Character Sheet (JSON):\n{current_state_json}\n\nRequested Changes:\n{requirements}"

        final_prompt = self.prompt_manager.build_entity_prompt(
            requirements=requirements,
            mode=mode,
            is_modification=is_modification
        )

        return self.llm_client.generate_structured_entity(final_prompt)
