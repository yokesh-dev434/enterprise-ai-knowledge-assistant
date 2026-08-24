# Enterprise AI Knowledge Assistant

An **Enterprise AI Knowledge Assistant** built using **Retrieval-Augmented Generation (RAG)**.

The system allows users to ask questions about enterprise documents and retrieves relevant information from a vector database before generating a context-aware answer using an LLM.

---

## Current Architecture

### Document Processing Flow

```text
Enterprise Documents
(PDF / DOCX)
        ↓
Document Processing
        ↓
Text Chunking
        ↓
Generate Embeddings
(Sentence Transformers)
        ↓
Qdrant Vector Database
(Vector + Metadata)
```

### User Query Flow

```text
User Question
        ↓
LLM Department Classifier
        ↓
Department + Confidence
        ↓
Qdrant Metadata Filtering
        ↓
Query Embedding
        ↓
Vector Similarity Search
        ↓
Relevant Document Chunks
        ↓
Similarity Threshold
        ↓
Gemini LLM
        ↓
Final Answer
```

---

# How the System Works

## 1. Document Ingestion

Enterprise documents are processed and divided into smaller text chunks.

```text
Employee Handbook
        ↓
Chunk 1
Chunk 2
Chunk 3
...
```

Chunking helps the system retrieve specific and relevant information instead of sending an entire document to the LLM.

---

## 2. Embedding Generation

Each document chunk is converted into a numerical vector representation using an embedding model.

```text
Text Chunk
    ↓
Embedding Model
    ↓
384-Dimensional Vector
```

These vector embeddings represent the semantic meaning of the document content.

---

## 3. Vector Storage

The generated embeddings are stored in **Qdrant** along with document metadata.

Example:

```json
{
    "text": "Employees must complete mandatory training.",
    "department": "HR",
    "source": "Employee_Handbook.docx",
    "page": 1,
    "file_type": "docx"
}
```

This metadata enables the system to perform filtered vector searches.

---

## 4. Department Classification

Before performing vector search, the user's query is classified into one of the supported enterprise departments.

### Supported Departments

* HR
* IT
* CLIENT
* ENG
* PROJECTS
* FINANCE
* UNKNOWN

The classifier also returns a confidence score.

Example:

```text
User Query:
"What is the maternity leave policy?"

        ↓

Department: HR
Confidence: 0.99
```

---

## 5. Metadata Filtering

The classified department is used to filter the Qdrant vector database.

Example:

```text
department = HR
```

The vector search retrieves documents only from the relevant department.

```text
Qdrant Search

Filter:
department = HR
```

This reduces unnecessary search results and improves retrieval accuracy.

---

## 6. Vector Similarity Search

The user query is converted into an embedding and compared against document embeddings.

```text
User Query
    ↓
Query Embedding
    ↓
Qdrant Search
    ↓
Top Relevant Chunks
```

The system retrieves the most semantically relevant document chunks.

---

## 7. Similarity Threshold

Retrieved chunks are checked against a similarity threshold.

```text
Retrieved Chunks
        ↓
Similarity Threshold
        ↓
Relevant Context
```

If no relevant context is found, the system can avoid generating answers based on unrelated information.

---

## 8. LLM Answer Generation

The retrieved document chunks are sent to the LLM together with the user's question.

```text
User Question
        +
Relevant Context
        ↓
Gemini LLM
        ↓
Final Answer
```

The final answer is generated using retrieved enterprise knowledge.

---

# Technologies Used

| Category               | Technology            |
| ---------------------- | --------------------- |
| Programming Language   | Python                |
| LLM Framework          | LangChain             |
| LLM                    | Google Gemini         |
| Structured Output      | Pydantic              |
| Embeddings             | Sentence Transformers |
| Vector Database        | Qdrant                |
| Vector Database Client | Qdrant Client         |
| Metadata Filtering     | Qdrant Filters        |
| Environment Variables  | python-dotenv         |

---

# Current Project Structure

```text
enterprise_ai_assistant/
│
├── app/
│   ├── config/
│   ├── exceptions/
│   ├── ingestion/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   │   ├── classifier_service.py
│   │   ├── document_processor.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── rag_service.py
│   │   └── vector_store.py
│   │
│   ├── uploads/
│   ├── main.py
│   └── test_rag.py
│
├── data/
├── sample.ipynb
├── .gitignore
└── README.md
```

---

# Current RAG Flow

```text
User Query
    ↓
Classifier Agent
    ↓
Department + Confidence
    ↓
Generate Query Embedding
    ↓
Qdrant Metadata Filter
    ↓
Vector Similarity Search
    ↓
Similarity Threshold
    ↓
Relevant Chunks
    ↓
Gemini LLM
    ↓
Final Answer
```

---

# Completed Features

* [x] Project structure
* [x] Document processing
* [x] Text chunking
* [x] Embedding generation
* [x] Qdrant vector storage
* [x] Metadata storage
* [x] Vector similarity search
* [x] Gemini LLM integration
* [x] LLM department classifier
* [x] Pydantic structured output
* [x] Qdrant metadata filtering
* [x] RAG service integration
* [x] GitHub repository setup

---

# Next Steps

* [ ] End-to-end testing
* [ ] Improve UNKNOWN query handling
* [ ] Add more department documents
* [ ] Multi-department query handling
* [ ] API integration and testing
* [ ] Improve error handling
* [ ] RAG evaluation
* [ ] User interface
* [ ] Production deployment

---

# Project Progress

## Core RAG Backend

```text
██████████████░░░░░░  ~70%
```

The core architecture and major RAG components are implemented.

The next phase focuses on:

* End-to-end testing
* Retrieval improvement
* UNKNOWN query handling
* Multi-department query support
* RAG evaluation
* API integration
* Error handling
* User interface development
* Production deployment

> **Current Status:** Core RAG Backend ~70% Complete

---

# Project Goal

The goal of this project is to build an enterprise knowledge assistant capable of retrieving relevant information from internal documents and generating accurate, context-aware answers using **Retrieval-Augmented Generation (RAG)**.

The project is designed to demonstrate concepts used in enterprise AI systems, including:

* Document ingestion
* Text chunking
* Embedding generation
* Vector databases
* Metadata filtering
* LLM-based query classification
* Structured LLM output
* Semantic search
* Retrieval-Augmented Generation

---

## Author

**Yokesh P**

AI Engineer | Python Developer | RAG | AI Agents | FastAPI

---

##  Current Status

  **Active Development**

The core RAG backend is implemented and the project is currently moving toward end-to-end testing, evaluation, API integration, and production-ready improvements.
