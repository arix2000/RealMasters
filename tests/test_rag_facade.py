import pytest
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document
from backend.rag_facade import RagFacade
from backend.models import CharacterSheet, EntityStats, SourceDocument

@pytest.fixture
def mock_managers():
    with patch("backend.rag_facade.DocumentProcessor") as mock_dp, \
         patch("backend.rag_facade.PromptAndGuardrailManager") as mock_pg, \
         patch("backend.rag_facade.LLMClient") as mock_lc, \
         patch("backend.rag_facade.VectorStoreManager") as mock_vm:
        yield {
            "dp": mock_dp.return_value,
            "pg": mock_pg.return_value,
            "lc": mock_lc.return_value,
            "vm": mock_vm.return_value
        }

def test_rag_facade_init(mock_managers):
    facade = RagFacade(api_key="key")
    assert facade.vector_manager is not None
    assert mock_managers["vm"].load_store.call_count == 2

def test_ingest_context_file(mock_managers):
    facade = RagFacade(api_key="key")
    mock_chunks = [Document(page_content="c")]
    mock_managers["dp"].process_file.return_value = mock_chunks
    
    facade.ingest_context_file(b"content", "test.txt", "player")
    mock_managers["vm"].add_custom_context.assert_called_with(mock_chunks, "player")

def test_process_chat_query(mock_managers):
    facade = RagFacade(api_key="key")
    mock_doc = Document(page_content="context content", metadata={"s": "m"})
    mock_managers["vm"].search_similar.return_value = [mock_doc]
    mock_managers["lc"].generate_chat_response.return_value = "answer text"
    
    response = facade.process_chat_query("query", "player")
    
    assert response.answer == "answer text"
    assert response.sources[0].content == "context content"
    mock_managers["pg"].check_guardrails.assert_called_with("query")

def test_generate_entity(mock_managers):
    facade = RagFacade(api_key="key")
    expected_sheet = CharacterSheet(
        name="N", role_or_class="R", race="R",
        stats=EntityStats(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10),
        background_story="B"
    )
    mock_managers["lc"].generate_structured_entity.return_value = expected_sheet
    
    result = facade.generate_entity("requirements", "player")
    assert result.name == "N"
    mock_managers["pg"].build_entity_prompt.assert_called()
