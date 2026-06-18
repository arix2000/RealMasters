import pytest
from backend.prompt_and_guardrail_manager import PromptAndGuardrailManager
from backend.exceptions import GuardrailViolationError, PromptFormattingError

def test_check_guardrails_length():
    mgr = PromptAndGuardrailManager()
    with pytest.raises(GuardrailViolationError) as excinfo:
        mgr.check_guardrails("a" * 1001)
    assert excinfo.value.details["attempt_type"] == "PayloadTooLarge"

def test_check_guardrails_forbidden():
    mgr = PromptAndGuardrailManager()
    with pytest.raises(GuardrailViolationError) as excinfo:
        mgr.check_guardrails("ignore instructions")
    assert excinfo.value.details["attempt_type"] == "RegexBlacklistMatch"

def test_check_guardrails_empty():
    mgr = PromptAndGuardrailManager()
    with pytest.raises(GuardrailViolationError) as excinfo:
        mgr.check_guardrails("   ")
    assert excinfo.value.details["attempt_type"] == "EmptyQuery"

def test_build_chat_prompt():
    mgr = PromptAndGuardrailManager()
    prompt = mgr.build_chat_prompt("query", "context", "player")
    assert "query" in prompt
    assert "context" in prompt
    assert "Player Assistant" in prompt

def test_build_entity_prompt():
    mgr = PromptAndGuardrailManager()
    prompt = mgr.build_entity_prompt("reqs", "master", is_modification=True)
    assert "modify" in prompt
    assert "reqs" in prompt
    assert "Game Master Advisor" in prompt

def test_build_chat_prompt_error():
    mgr = PromptAndGuardrailManager()
    with pytest.raises(PromptFormattingError):
        mgr.build_chat_prompt("q", "c", "invalid_mode")
