import pytest
from unittest.mock import MagicMock, patch
from backend.llm_client import LLMClient
from backend.exceptions import UpstreamAPIError, StructuredParsingError
from backend.models import CharacterSheet, EntityStats

@pytest.fixture
def mock_llm_configs():
    with patch("backend.llm_client.ChatGoogleGenerativeAI") as mock_chat:
        yield mock_chat

def test_llm_client_init_error(mock_llm_configs):
    mock_llm_configs.side_effect = Exception("error")
    with pytest.raises(UpstreamAPIError):
        LLMClient(api_key="key")

def test_generate_chat_response(mock_llm_configs):
    mock_instance = mock_llm_configs.return_value
    mock_instance.invoke.return_value.content = "response content"
    
    client = LLMClient(api_key="key")
    resp = client.generate_chat_response("prompt")
    assert resp == "response content"

def test_generate_chat_response_error(mock_llm_configs):
    mock_instance = mock_llm_configs.return_value
    mock_instance.invoke.side_effect = Exception("API Error")
    
    client = LLMClient(api_key="key")
    with pytest.raises(UpstreamAPIError):
        client.generate_chat_response("prompt")

def test_generate_structured_entity(mock_llm_configs):
    mock_instance = mock_llm_configs.return_value
    mock_structured = mock_instance.with_structured_output.return_value
    
    expected_sheet = CharacterSheet(
        name="N", role_or_class="R", race="R",
        stats=EntityStats(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10),
        background_story="B"
    )
    mock_structured.invoke.return_value = expected_sheet
    
    client = LLMClient(api_key="key")
    result = client.generate_structured_entity("prompt")
    assert result.name == "N"

def test_generate_structured_entity_error(mock_llm_configs):
    mock_instance = mock_llm_configs.return_value
    mock_structured = mock_instance.with_structured_output.return_value
    mock_structured.invoke.side_effect = Exception("Parsing Error")
    
    client = LLMClient(api_key="key")
    with pytest.raises(StructuredParsingError):
        client.generate_structured_entity("prompt")
