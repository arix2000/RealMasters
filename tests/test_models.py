import pytest
from pydantic import ValidationError
from backend.models import SourceDocument, ChatResponse, EntityStats, CharacterSheet

def test_source_document_valid():
    doc = SourceDocument(content="test content", metadata={"source": "test.txt"})
    assert doc.content == "test content"
    assert doc.metadata["source"] == "test.txt"

def test_source_document_default_metadata():
    doc = SourceDocument(content="test content")
    assert doc.metadata == {}

def test_chat_response_valid():
    sources = [SourceDocument(content="c", metadata={"m": "v"})]
    resp = ChatResponse(answer="ans", sources=sources, is_guardrail_triggered=False)
    assert resp.answer == "ans"
    assert len(resp.sources) == 1

def test_entity_stats_valid():
    stats = EntityStats(strength=10, dexterity=11, constitution=12, intelligence=13, wisdom=14, charisma=15)
    assert stats.strength == 10

def test_character_sheet_valid():
    stats = EntityStats(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10)
    sheet = CharacterSheet(
        name="Name",
        role_or_class="Role",
        race="Race",
        stats=stats,
        background_story="Story",
        equipment=["Sword"]
    )
    assert sheet.name == "Name"
    assert sheet.equipment == ["Sword"]
    assert sheet.special_traits is None

def test_character_sheet_invalid():
    with pytest.raises(ValidationError):
        CharacterSheet(name="Name", role_or_class="Role", race="Race", stats={"strength": "invalid"})
