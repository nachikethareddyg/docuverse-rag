# Demo Guide

This guide captures the exact Windows PowerShell path for running docuverse-rag
locally and taking screenshots for the README demo section.

## 1. Prepare The Environment

```powershell
cd C:\Projects\docuverse-rag
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Run the test suite before recording screenshots:

```powershell
python -m pytest
```

## 2. Start Postgres With pgvector

```powershell
docker compose up -d postgres
```

The compose file uses the `pgvector/pgvector:pg16` image and runs
`docker/postgres/init.sql` to enable the `vector` extension.

## 3. Ingest, Embed, And Store Documents

```powershell
python -m docuverse.store data/corpus_aws
```

This command loads the sample AWS markdown files, chunks them, creates
embeddings, initializes the database schema, clears old rows, and stores the
current chunk set.

## 4. Set OPENAI_API_KEY

Set an OpenAI API key:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

## 5. Ask Questions From The CLI

Generate an answer:

```powershell
python -m docuverse.answer "What is AWS S3?"
```

Retrieve chunks directly:

```powershell
python -m docuverse.retrieve "What is AWS S3?"
```

## 6. Run The FastAPI Service

```powershell
python -m uvicorn docuverse.api:app --reload
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Ask endpoint:

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

## 7. Run The Streamlit UI

```powershell
streamlit run src/docuverse/ui.py
```

Use the sample question:

```text
What is AWS S3?
```

## 8. Capture README Screenshots

Save screenshots in `docs/images/` with these filenames:

```text
docs/images/ui-home.png
docs/images/answer-example.png
docs/images/retrieval-example.png
docs/images/api-example.png
```

Suggested captures:

- `ui-home.png`: Streamlit app loaded with the question box and `top_k` slider
- `answer-example.png`: generated answer with visible citations
- `retrieval-example.png`: expanded retrieved sources/chunks section
- `api-example.png`: `/ask` response from PowerShell, browser, or API client

Keep screenshots cropped tightly around the useful UI. Recruiters should be able
to understand the system at a glance without reading every command.

## Recommended GitHub Topics

Add these topics to the GitHub repository sidebar:

```text
rag
fastapi
streamlit
postgresql
pgvector
vector-search
llm
python
openai
```
