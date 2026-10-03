# Enterprise AI Knowledge Assistant

An enterprise-style multi-document Retrieval-Augmented Generation (RAG) application that allows authenticated users to ask questions about internal company documents about internal company documents and receive relevant, context-aware answers.

The application supports PDF, DOCX, and TXT documents. Documents are processed, cleaned, chunked, converted into vector embeddings, and stored in Qdrant for semantic search.

User queries are processed through query rewriting, department classification, vector retrieval, and Gemini-based answer generation.

The application also includes JWT-based authentication, Redis-powered conversation memory, source/page references, a FastAPI backend, and a Streamlit frontend.

---

## Features

- Multi-document RAG
- PDF, DOCX, and TXT document support
- Document text extraction and cleaning
- Recursive text chunking
- Hugging Face sentence embeddings
- Qdrant vector database
- Department-based document filtering
- Semantic similarity search
- Similarity threshold filtering
- Query rewriting for conversational questions
- Department classification using Gemini structured output
- Gemini-powered answer generation
- Hallucination-control prompt
- Source and page references
- Redis conversation memory
- JWT-based authentication
- Streamlit chat interface
- Document upload interface
- Recent chat sessions
- New chat functionality
- Fallback handling for unavailable or irrelevant information
- Docker-based Qdrant and Redis services

---

## Architecture

```text
                         ┌─────────────────────┐
                         │      Employee       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Streamlit UI      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FastAPI API      │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
             ┌───────────────┐             ┌───────────────┐
             │     Redis     │             │ Authentication│
             │ Chat Memory   │             │     / JWT     │
             └───────┬───────┘             └───────────────┘
                     │
                     ▼
             ┌───────────────────┐
             │ Standalone Query  │
             │     Rewriting     │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │    Department     │
             │   Classification  │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ Hugging Face      │
             │ Embedding Model   │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │      Qdrant       │
             │   Vector Search   │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ Similarity Filter │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ Gemini LLM        │
             │ Answer Generation │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ Answer + Sources  │
             │   + Page Number   │
             └───────────────────┘
```
### RAG Pipeline

The application follows a complete Retrieval-Augmented Generation pipeline.

Document
   ↓
Text Extraction
   ↓
Text Cleaning
   ↓
Chunking
   ↓
Embedding Generation
   ↓
Qdrant Vector Database
   ↓
User Query
   ↓
Query Rewriting
   ↓
Department Classification
   ↓
Query Embedding
   ↓
Department-Filtered Retrieval
   ↓
Similarity Threshold
   ↓
Relevant Context
   ↓
Gemini
   ↓
Final Answer
1. Document Ingestion

The application accepts:

PDF
DOCX
TXT

Uploaded documents are processed before being stored in the vector database.

Processing flow
Upload Document
      ↓
Extract Text
      ↓
Clean Text
      ↓
Split Into Chunks
      ↓
Generate Embeddings
      ↓
Store in Qdrant

For PDF documents, page numbers are preserved during extraction.

For DOCX documents, the document is converted to PDF before page-based extraction.

2. Text Chunking

Documents are divided into smaller chunks using:

RecursiveCharacterTextSplitter

Current configuration:

Chunk Size: 800
Chunk Overlap: 100

Chunking allows the retrieval system to search for relevant sections of documents instead of passing entire documents to the LLM.

Each stored chunk contains metadata such as:

document_id
chunk_index
department
source
file_type
page
text
3. Embeddings

The project uses the Hugging Face embedding model:

sentence-transformers/all-MiniLM-L6-v2

Embedding dimension:

384

Each document chunk is converted into a 384-dimensional vector.

The user's query is also converted into a vector before semantic search.

4. Vector Database

The project uses:

Qdrant

Collection:

knowledge_v1

Vector configuration:

Dimension: 384
Distance: COSINE

Qdrant is used to perform semantic similarity search over document chunks.

5. Department Classification

Before retrieving documents, the user's standalone query is classified into a department.

Supported classifications include:

HR
IT
Client
Engineering
PROJECTS
Finance
UNKNOWN
GREETING
ACKNOWLEDGEMENT

The classifier uses Gemini structured output with a Pydantic schema.

Example:

User:
"How many days of leave can I take?"

Classification:
HR

The department classification is then used to filter the Qdrant search.

This helps prevent retrieval from unrelated departments.

6. Conversational Query Rewriting

The application supports conversational questions.

For example:

User:
"What is the VPN procedure?"

Assistant:
Provides VPN procedure.

User:
"Where can I find it?"

The second question may not contain enough information by itself.

The application uses the previous conversation history to rewrite the query into a standalone question before retrieval.

Conceptually:

User Query
     +
Conversation History
     ↓
Standalone Query

This improves retrieval for follow-up questions.

7. Semantic Retrieval

After query rewriting and department classification:

User Query
     ↓
Embedding
     ↓
Qdrant Search
     ↓
Department Filter
     ↓
Top 3 Results

The current retrieval configuration uses:

Top K = 3

Only relevant results above the configured similarity threshold are passed to the LLM.

Current threshold:

0.25
8. Answer Generation

Retrieved document chunks are provided to Gemini as context.

The generation prompt instructs the model to:

Use retrieved company documents as the source of truth
Avoid making up information
Avoid unsupported assumptions
Keep answers concise
Return a fallback response when sufficient information is unavailable

If relevant information cannot be found, the application returns:

I couldn't find enough relevant information in the available documents.
Conversation Memory

Redis is used to maintain conversation history.

The application stores conversation turns containing:

{
    "user": "...",
    "assistant": "..."
}

The current implementation keeps the latest 5 conversation turns for a session.

Redis is also used to maintain available chat sessions.

Conversation history is used by the standalone query rewriting component to understand follow-up questions.

Authentication

The application uses JWT-based authentication.

Protected endpoints require a valid JWT token.

Authentication flow:

Login
  ↓
Validate Credentials
  ↓
Generate JWT
  ↓
Client Stores Token
  ↓
Token Sent With API Requests
  ↓
FastAPI Validates Token
  ↓
Protected Endpoint Access

The current project uses a simple demo login credential rather than a database-backed employee/user management system.

Production improvements would include:

Database-backed users
Password hashing
Employee registration/management
Role-based access control
User-specific permissions
Source References

The application returns source information along with answers.

Example:

Answer:
Probation confirmation is approved by the Reporting Manager and HRBP.

Sources:
Employee_Handbook - Page 2

This allows users to identify where the retrieved information came from.

### Project Structure
enterprise-ai-knowledge-assistant/
│
├── app/
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── document.py
│   │   └── login.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── login.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── classifier_service.py
│   │   ├── document_processor.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── llm_service.py
│   │   ├── rag_service.py
│   │   ├── redis_service.py
│   │   ├── standalone_service.py
│   │   └── vector_store.py
│   │
│   ├── ingestion/
│   │   └── ingest_document.py
│   │
│   └── main.py
│
├── app_pages/
│   ├── chat.py
│   └── document_upload.py
│
├── data/
│   └── documents/
│
├── streamlit_app.py
├── requirements.txt
├── .gitignore
├── requirements.txt
└── README.md
## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | Google Gemini |
| LLM Framework | LangChain |
| Embeddings | Hugging Face Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | Qdrant |
| Cache / Memory | Redis |
| Authentication | JWT |
| Document Processing | PyMuPDF, python-docx, docx2pdf |
| Text Splitting | RecursiveCharacterTextSplitter |
| Data Validation | Pydantic |
| Containerization | Docker |
| Version Control | Git / GitHub |

Used to authenticate the user and generate a JWT token.

Chat
Get Chat Sessions
GET /chat/sessions

Returns available chat sessions.

Get Session Conversation
GET /chat/sessions/{session_id}

Returns conversation history for a specific session.

Chat
POST /chat/main_chat

Processes the user query through the RAG pipeline and returns:

{
    "session_id": "...",
    "final_answer": "...",
    "sources": []
}
Documents
Upload Document
POST /documents/

Uploads and ingests a PDF, DOCX, or TXT document.

The endpoint accepts a department along with the document.

Supported departments:

HR
IT
Finance
Engineering
Client
PROJECTS
Running the Project
Prerequisites

Install the following:

Python
Docker
Git

You also need a Google Gemini API key.

1. Clone the Repository
git clone https://github.com/yokesh-dev434/enterprise-ai-knowledge-assistant.git
cd enterprise-ai-knowledge-assistant
2. Create a Virtual Environment

Windows:

python -m venv ent_ai_env

Activate it:

ent_ai_env\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Environment Variables

Create a .env file in the project root.

APP_NAME=Enterprise AI Knowledge Assistant
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key

Do not commit the .env file to GitHub.

5. Start Qdrant

Run Qdrant using Docker:

docker run -p 6333:6333 qdrant/qdrant

Qdrant will be available at:

http://localhost:6333
6. Start Redis

Run Redis using Docker:

docker run -d --name redis -p 6379:6379 redis

Redis will be available at:

localhost:6379
7. Start FastAPI

Run:

uvicorn app.main:app --reload

FastAPI will run at:

http://127.0.0.1:8000

Swagger API documentation:

http://127.0.0.1:8000/docs
8. Start Streamlit

Open another terminal and run:

streamlit run streamlit_app.py

The Streamlit application will open in the browser.

Application Workflow
Document Upload
Login
  ↓
Document Upload
  ↓
Select Department
  ↓
Upload PDF/DOCX/TXT
  ↓
Text Extraction
  ↓
Cleaning
  ↓
Chunking
  ↓
Embedding Generation
  ↓
Qdrant Storage
Question Answering
Login
  ↓
Ask Question
  ↓
Retrieve Conversation History
  ↓
Rewrite Query
  ↓
Classify Department
  ↓
Generate Query Embedding
  ↓
Search Qdrant
  ↓
Apply Similarity Threshold
  ↓
Retrieve Relevant Chunks
  ↓
Gemini
  ↓
Answer + Sources
  ↓
Store Conversation in Redis
Example

Suppose the company has an internal VPN document.

The employee asks:

How do employees connect to the VPN?

The system:

1. Receives the question
2. Classifies it as IT
3. Generates an embedding
4. Searches IT documents in Qdrant
5. Retrieves relevant chunks
6. Applies the similarity threshold
7. Sends the relevant context to Gemini
8. Generates the answer
9. Returns the source and page number
10. Stores the conversation in Redis
Error and Fallback Handling

The application includes fallback handling for several situations.

Unknown Department

If the classifier cannot identify a relevant department:

I couldn't identify a relevant department for your question.
Insufficient Retrieval

If no retrieved chunks pass the similarity threshold:

I couldn't find enough relevant information in the available documents.
LLM Failure

If the primary Gemini generation fails, the application attempts to use a fallback model.

If the fallback also fails, the application returns a temporary service-unavailable response.

Invalid Authentication

Invalid or expired JWT tokens result in an authentication error.

Design Decisions
Why RAG?

Company information can change and may exist across many internal documents.

Instead of relying only on the LLM's pretrained knowledge, the system retrieves relevant company information from the organization's documents before generating an answer.

This helps ground responses in the available company knowledge.

Why Qdrant?

Qdrant provides vector similarity search and supports metadata filtering.

The project uses department metadata to restrict retrieval to relevant organizational areas.

Why Redis?

Redis provides fast storage for conversation history.

It is used to maintain recent conversation turns and support conversational query rewriting.

Why FastAPI?

FastAPI provides:

API development
Request validation
Authentication dependencies
Swagger documentation
Easy integration with Python-based AI services
Why Streamlit?

Streamlit provides a simple interface for demonstrating the AI assistant without building a separate frontend application.

Current Limitations

The current implementation is designed as a portfolio/project implementation rather than a complete production deployment.

Current limitations include:

Demo/static login credentials
No database-backed employee management
No role-based access control
Redis sessions are not user-isolated
Conversation sources are not persisted with Redis conversation history
Local Qdrant deployment
Local Redis deployment
Limited document formats
No production monitoring system
No automated evaluation framework for retrieval quality
Similarity threshold is manually configured
Confidence returned by the classifier is model-generated and not calibrated
Future Improvements

Possible future improvements include:

Database-backed employee authentication
Password hashing
Role-based access control
User-specific chat sessions
Persistent conversation sources
PostgreSQL integration
Batch document ingestion
Improved metadata filtering
Retrieval quality evaluation
Reranking models
Hybrid search
Better chunking strategies
Production Qdrant deployment
Redis production configuration
API monitoring and logging
Automated RAG evaluation
Deployment using cloud infrastructure
CI/CD pipeline
Kubernetes deployment
Project Goals

The main goal of this project was to build an end-to-end enterprise AI application rather than only a basic chatbot.

The project demonstrates the integration of:

LLM
+
RAG
+
Embeddings
+
Vector Database
+
Metadata Filtering
+
Query Rewriting
+
Conversation Memory
+
FastAPI
+
Authentication
+
Streamlit
+
Docker

This project was developed to understand how an enterprise-oriented AI knowledge assistant can be designed from document ingestion to user-facing question answering.

Key Learning Outcomes

Through this project, I worked with:

RAG architecture
Document ingestion pipelines
PDF/DOCX/TXT processing
Text chunking
Embedding generation
Vector databases
Semantic search
Metadata filtering
LLM integration
Structured LLM output
Query rewriting
Conversation memory
Redis
FastAPI
JWT authentication
Streamlit
Docker
Git/GitHub
API integration
Error handling
Source attribution
Repository

GitHub:

https://github.com/yokesh-dev434/enterprise-ai-knowledge-assistant

Author

Yokesh P

AI Engineer | Python Developer | RAG | AI Agents | FastAPI