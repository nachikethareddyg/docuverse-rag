# docuverse-rag

docuverse-rag is a Python 3.11 project for a document question-answering system.
Phase 1 provides a minimal runnable FastAPI skeleton with a health check endpoint,
pytest coverage, Docker support, and a Postgres 16 service with the pgvector
extension enabled.

## How to run locally

Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project:

```powershell
python -m pip install --upgrade pip
python -m pip install -e .
```

Run the tests:

```powershell
python -m pytest
```

Start the FastAPI app:

```powershell
python -m uvicorn docuverse.api:app --reload
```

Start Postgres with pgvector:

```powershell
docker compose up -d postgres
```

Store embedded chunks in Postgres with pgvector:

```powershell
python -m docuverse.store data/corpus_aws
```

Retrieve similar chunks:

```powershell
python -m docuverse.retrieve "What is AWS S3?"
```

Generate an answer with citations:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
python -m docuverse.answer "What is AWS S3?"
```

## Health endpoint example

After starting the FastAPI app, check the health endpoint:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Ask endpoint example

After storing embedded chunks and setting `OPENAI_API_KEY`, ask a question through
the API:

```powershell
$body = @{
    question = "What is AWS S3?"
    top_k = 5
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://127.0.0.1:8000/ask `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```
