from fastapi import FastAPI


app = FastAPI(title="docuverse-rag")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
