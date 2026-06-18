from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.exceptions import EmptyDocumentError, TextProcessingError

class DocumentProcessor:

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )

    def process_file(self, file_bytes: bytes, filename: str) -> List[Document]:
        raw_text = self._decode_and_validate(file_bytes, filename)

        return self._split_into_chunks(raw_text, filename)

    def _split_into_chunks(self, text: str, filename: str) -> List[Document]:
        try:
            metadata = {"source": filename, "type": "user_upload"}

            text_chunks = self.text_splitter.split_text(text)

            documents = [
                Document(page_content=chunk, metadata=metadata)
                for chunk in text_chunks
            ]

            return documents

        except Exception as e:
            raise TextProcessingError(
                filename=filename,
                chunking_strategy=f"RecursiveCharacter(size={self.chunk_size})"
            )

    @staticmethod
    def _decode_and_validate(file_bytes: bytes, filename: str) -> str:
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise TextProcessingError(
                filename=filename,
                chunking_strategy="Decode",
            )

        text = " ".join(text.split())

        if not text or len(text) < 50:
            raise EmptyDocumentError(filename=filename, file_size=len(text))

        return text
