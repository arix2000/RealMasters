import logging

logger = logging.getLogger("LoreMaster.Backend")


class LoreMasterBaseError(Exception):
    def __init__(self, dev_message: str, **kwargs):
        self.dev_message = dev_message
        self.details = kwargs

        details_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])

        log_msg = f"{self.__class__.__name__}: {dev_message}"
        if details_str:
            log_msg += f" | Szczegóły: [{details_str}]"

        logger.error(log_msg)

        super().__init__(self.dev_message)


class EmptyDocumentError(LoreMasterBaseError):
    def __init__(self, filename: str, file_size: int):
        self.filename = filename
        self.file_size = file_size

        super().__init__(
            dev_message="Plik wejściowy nie zawiera wystarczającej ilości tekstu.",
            filename=filename,
            file_size=file_size
        )


class TextProcessingError(LoreMasterBaseError):
    def __init__(self, filename: str, chunking_strategy: str):
        self.filename = filename
        super().__init__(
            dev_message="Wystąpił krytyczny błąd podczas podziału tekstu na wektory.",
            filename=filename,
            chunking_strategy=chunking_strategy
        )


class GuardrailViolationError(LoreMasterBaseError):
    def __init__(self, attempt_type: str, blocked_query: str):
        self.attempt_type = attempt_type
        super().__init__(
            dev_message="Zapytanie zablokowane przez filtry bezpieczeństwa (Guardrails).",
            attempt_type=attempt_type,
            blocked_query=blocked_query
        )


class MissingContextError(LoreMasterBaseError):
    def __init__(self, mode: str, query: str):
        super().__init__(
            dev_message="Baza RAG nie zwróciła żadnych trafnych wyników dla tego zapytania.",
            mode=mode,
            query=query
        )


class UpstreamAPIError(LoreMasterBaseError):
    def __init__(self, provider: str, status_code: int):
        self.status_code = status_code
        super().__init__(
            dev_message="Zewnętrzne API modelu LLM odrzuciło żądanie.",
            provider=provider,
            status_code=status_code
        )


class StructuredParsingError(LoreMasterBaseError):
    def __init__(self, target_model: str, raw_output: str):
        super().__init__(
            dev_message="LLM zwrócił format, którego Pydantic nie potrafi zmapować na schemat.",
            target_model=target_model,
            raw_output=raw_output
        )

class EmbeddingModelError(LoreMasterBaseError):
    def __init__(self, model_name: str, error_details: str):
        self.model_name = model_name
        self.error_details = error_details
        super().__init__(
            dev_message="Nie udało się załadować lokalnego modelu wektoryzującego (HuggingFace) do pamięci.",
            model_name=model_name,
            error_details=error_details
        )


class VectorStoreLoadError(LoreMasterBaseError):
    def __init__(self, mode: str, file_path: str):
        self.mode = mode
        self.file_path = file_path
        super().__init__(
            dev_message="Nie udało się załadować bazy FAISS z dysku. Plik nie istnieje, brak uprawnień lub format jest uszkodzony.",
            mode=mode,
            file_path=file_path
        )


class VectorStoreOperationError(LoreMasterBaseError):
    def __init__(self, operation: str, mode: str, details: str):
        self.operation = operation
        self.mode = mode
        self.details = details
        super().__init__(
            dev_message="Krytyczny błąd podczas operacji na wektorach w pamięci RAM.",
            operation=operation,
            mode=mode,
            details=details
        )
