import pytest
from backend.document_processor import DocumentProcessor
from backend.exceptions import EmptyDocumentError, TextProcessingError

def test_document_processor_init():
    dp = DocumentProcessor(chunk_size=100, chunk_overlap=20)
    assert dp.chunk_size == 100
    assert dp.chunk_overlap == 20

def test_decode_and_validate_success():
    dp = DocumentProcessor()
    text = "A" * 50
    result = dp._decode_and_validate(text.encode("utf-8"), "test.txt")
    assert result == text

def test_decode_and_validate_unicode_error():
    dp = DocumentProcessor()
    with pytest.raises(TextProcessingError) as excinfo:
        dp._decode_and_validate(b"\xff", "test.txt")
    assert excinfo.value.details["chunking_strategy"] == "Decode"

def test_decode_and_validate_empty_error():
    dp = DocumentProcessor()
    with pytest.raises(EmptyDocumentError):
        dp._decode_and_validate(b"too short", "test.txt")

def test_split_into_chunks():
    dp = DocumentProcessor(chunk_size=50, chunk_overlap=0)
    text = "A" * 100
    docs = dp._split_into_chunks(text, "test.txt")
    assert len(docs) >= 2
    assert docs[0].metadata["source"] == "test.txt"

def test_process_file():
    dp = DocumentProcessor(chunk_size=100, chunk_overlap=10)
    content = ("Long text that should be enough for the validation check to pass " * 2).encode("utf-8")
    docs = dp.process_file(content, "test.txt")
    assert len(docs) > 0
    assert docs[0].page_content is not None
