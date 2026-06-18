import pytest
import os
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document
from backend.vector_manager import VectorStoreManager
from backend.exceptions import (
    EmbeddingModelError,
    VectorStoreLoadError,
    VectorStoreOperationError,
    MissingContextError
)

@pytest.fixture
def mock_embeddings():
    with patch("backend.vector_manager.HuggingFaceEmbeddings") as mock:
        yield mock

@pytest.fixture
def mock_faiss():
    with patch("backend.vector_manager.FAISS") as mock:
        yield mock

def test_vector_manager_init_error(mock_embeddings):
    mock_embeddings.side_effect = Exception("Embed error")
    with pytest.raises(EmbeddingModelError):
        VectorStoreManager()

def test_load_store_not_found(mock_embeddings):
    mgr = VectorStoreManager()
    with pytest.raises(VectorStoreLoadError):
        mgr.load_store("player", "nonexistent.index", "nonexistent.json")

def test_load_store_success(mock_embeddings, mock_faiss):
    mgr = VectorStoreManager()
    with patch("os.path.exists", return_value=True):
        mgr.load_store("player", "data/player.index", "data/player_chunks.json")
    assert mgr.stores["player"] is not None

def test_add_custom_context_uninitialized(mock_embeddings):
    mgr = VectorStoreManager()
    with pytest.raises(VectorStoreOperationError) as excinfo:
        mgr.add_custom_context([Document(page_content="test")], "player")
    assert "niezainicjalizowanej" in excinfo.value.details["details"]

def test_add_custom_context_success(mock_embeddings):
    mgr = VectorStoreManager()
    mock_store = MagicMock()
    mgr.stores["player"] = mock_store
    mgr.add_custom_context([Document(page_content="test")], "player")
    mock_store.add_documents.assert_called_once()

def test_search_similar_success(mock_embeddings):
    mgr = VectorStoreManager()
    mock_store = MagicMock()
    expected_docs = [Document(page_content="result")]
    mock_store.similarity_search.return_value = expected_docs
    mgr.stores["player"] = mock_store
    
    results = mgr.search_similar("query", "player")
    assert results == expected_docs

def test_search_similar_missing_context(mock_embeddings):
    mgr = VectorStoreManager()
    mock_store = MagicMock()
    mock_store.similarity_search.return_value = []
    mgr.stores["player"] = mock_store
    
    with pytest.raises(MissingContextError):
        mgr.search_similar("query", "player")
