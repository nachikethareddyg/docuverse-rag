from fastapi import FastAPI
from pydantic import BaseModel, Field

from docuverse.answer import generate_answer


app = FastAPI(title="docuverse-rag")


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class AskResponse(BaseModel):
    answer: str
    citations: list[str]
    sources: list[dict]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    result = generate_answer(request.question, top_k=request.top_k)
    return AskResponse(**result)
