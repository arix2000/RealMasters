import pytest
import logging
from backend.exceptions import (
    LoreMasterBaseError,
    EmptyDocumentError,
    TextProcessingError,
    GuardrailViolationError,
    MissingContextError,
    UpstreamAPIError,
    StructuredParsingError,
    EmbeddingModelError,
    VectorStoreLoadError,
    VectorStoreOperationError,
    PromptFormattingError
)

def test_lore_master_base_error():
    err = LoreMasterBaseError("test message", key="value")
    assert str(err) == "test message"
    assert err.details == {"key": "value"}

def test_empty_document_error():
    err = EmptyDocumentError("test.txt", 10)
    assert err.filename == "test.txt"
    assert err.file_size == 10
    assert "nie zawiera wystarczającej ilości tekstu" in err.dev_message

def test_text_processing_error():
    err = TextProcessingError("test.txt", "strategy")
    assert err.filename == "test.txt"
    assert "krytyczny błąd" in err.dev_message

def test_guardrail_violation_error():
    err = GuardrailViolationError("Type", "query")
    assert err.attempt_type == "Type"
    assert "zablokowane przez filtry" in err.dev_message

def test_missing_context_error():
    err = MissingContextError("player", "query")
    assert "nie zwróciła żadnych trafnych wyników" in err.dev_message

def test_upstream_api_error():
    err = UpstreamAPIError("Google", 500)
    assert err.status_code == 500
    assert "odrzuciło żądanie" in err.dev_message

def test_structured_parsing_error():
    err = StructuredParsingError("Model", "raw")
    assert "nie potrafi zmapować" in err.dev_message

def test_embedding_model_error():
    err = EmbeddingModelError("model", "error")
    assert err.model_name == "model"
    assert err.error_details == "error"

def test_vector_store_load_error():
    err = VectorStoreLoadError("player", "path")
    assert err.mode == "player"
    assert err.file_path == "path"

def test_vector_store_operation_error():
    err = VectorStoreOperationError("ADD", "player", "details")
    assert err.operation == "ADD"
    assert err.mode == "player"
    assert err.details["details"] == "details"

def test_prompt_formatting_error():
    err = PromptFormattingError("template", "variable")
    assert err.template_name == "template"
    assert err.missing_variable == "variable"
