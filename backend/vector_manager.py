import os
from typing import List, Dict, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import faiss
import json
import uuid
from langchain_community.docstore.in_memory import InMemoryDocstore

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
            index = faiss.read_index(index_path)

            with open(chunks_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)

            documents = []
            for chunk in chunks:
                if isinstance(chunk, str):
                    documents.append(Document(page_content=chunk, metadata={"source": f"{mode}_context"}))
                elif isinstance(chunk, dict) and "page_content" in chunk:
                    documents.append(Document(**chunk))
                else:
                    documents.append(Document(page_content=str(chunk), metadata={"source": f"{mode}_context"}))

            index_to_docstore_id = {i: str(uuid.uuid4()) for i in range(len(documents))}
            docstore = InMemoryDocstore({
                id_: doc for id_, doc in zip(index_to_docstore_id.values(), documents)
            })

            store = FAISS(
                embedding_function=self.embedder,
                index=index,
                docstore=docstore,
                index_to_docstore_id=index_to_docstore_id
            )
            self.stores[mode] = store

        except Exception as e:
            raise VectorStoreLoadError(mode=mode, file_path=str(e))

    def add_custom_context(self, chunks: List[Document], mode: AppMode) -> None:
        store = self.stores.get(mode)
        if not store:
            raise VectorStoreOperationError(
                operation="ADD",
                mode=mode,
                details="Próba zapisu do niezainicjalizowanej bazy."
            )

        try:
            store.add_documents(chunks)
        except Exception as e:
            raise VectorStoreOperationError(
                operation="ADD",
                mode=mode,
                details=str(e)
            )

    def search_similar(self, query: str, mode: AppMode, k: int = 3) -> List[Document]:
        store = self.stores.get(mode)
        if not store:
            raise VectorStoreOperationError(
                operation="SEARCH",
                mode=mode,
                details="Próba wyszukiwania w niezainicjalizowanej bazie."
            )

        try:
            results = store.similarity_search(query, k=k)
        except Exception as e:
            raise VectorStoreOperationError(
                operation="SEARCH",
                mode=mode,
                details=str(e)
            )

        if not results:
            raise MissingContextError(mode=mode, query=query)

        return results