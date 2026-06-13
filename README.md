# RealMasters Streamlit Project

## Setup

1. Create a conda environment:
   ```bash
   conda create -n realmasters python=3.11
   conda activate realmasters
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
streamlit run app.py
```

## Architecture & Design

### RAG Facade
The core communication with the RAG (Retrieval-Augmented Generation) engine happens through the `RagFacade` class (`backend/rag_facade.py`). It serves as a unified interface to:
- Ingest context documents into the vector store (`ingest_context_file`).
- Process natural language queries with context-awareness (`process_chat_query`).
- Generate structured entities like character sheets (`generate_entity`).

It maintains separate vector stores for `player` and `master` modes, keeping data isolated.

### Schema Definitions
Data structures are defined using Pydantic models in `backend/models.py`. Key schemas include:
- **`ChatResponse`**: Represents a response from the LLM, including the generated answer, source documents, and guardrail flags.
- **`CharacterSheet`**: A structured definition for a generated entity, including stats (`EntityStats`), background, equipment, and special traits.

### Exception Handling
The project implements a custom exception hierarchy in `backend/exceptions.py`, all inheriting from `LoreMasterBaseError`. This base class automatically logs errors. Common exceptions include:
- `EmptyDocumentError` / `TextProcessingError`: Thrown during file ingestion issues.
- `GuardrailViolationError`: Raised when user queries violate safety or thematic boundaries.
- `MissingContextError`: Thrown when the vector store lacks relevant data for a query.
- `StructuredParsingError`: Occurs when the LLM's output cannot be parsed into the expected Pydantic schema.
- `UpstreamAPIError`: Raised when the external LLM API fails or rejects the request.
