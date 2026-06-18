import os
from typing import List, Dict, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from backend.models import AppMode
from backend.exceptions import (
    EmbeddingModelError,
    VectorStoreLoadError,
    VectorStoreOperationError,
    MissingContextError
)


class VectorStoreManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        try:
            self.embedder = HuggingFaceEmbeddings(model_name=model_name)
        except Exception as e:
            raise EmbeddingModelError(model_name=model_name, error_details=str(e))

        self.stores: Dict[AppMode, Optional[FAISS]] = {
            'player': None,
            'master': None
        }

    def load_store(self, mode: AppMode, index_path: str, chunks_path: str) -> None:
        if not os.path.exists(index_path) or not os.path.exists(chunks_path):
            raise VectorStoreLoadError(mode=mode, file_path=index_path)

        try:
            folder_path = os.path.dirname(index_path)
            index_name = os.path.splitext(os.path.basename(index_path))[0]

            store = FAISS.load_local(
                folder_path=folder_path,
                embeddings=self.embedder,
                index_name=index_name,
                allow_dangerous_deserialization=True
            )
            self.stores[mode] = store

        except Exception as e:
            raise VectorStoreLoadError(mode=mode, file_path=str(e))

    def add_custom_context(self, chunks: List[Document], mode: AppMode) -> None:
        store = self.stores.get(mode)
        if not store:
            raise VectorStoreOperationError(
                operation="ADD", mode=mode, details="Próba zapisu do niezainicjalizowanej bazy."
            )

        try:
            store.add_documents(chunks)
        except Exception as e:
            raise VectorStoreOperationError(
                operation="ADD", mode=mode, details=str(e)
            )

    def search_similar(self, query: str, mode: AppMode, k: int = 3) -> List[Document]:
        store = self.stores.get(mode)
        if not store:
            raise VectorStoreOperationError(
                operation="SEARCH", mode=mode, details="Próba wyszukiwania w niezainicjalizowanej bazie."
            )

        try:
            results = store.similarity_search(query, k=k)
        except Exception as e:
            raise VectorStoreOperationError(
                operation="SEARCH", mode=mode, details=str(e)
            )

        if not results:
            raise MissingContextError(mode=mode, query=query)

        return results