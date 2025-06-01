from pydantic import BaseModel


class Question(BaseModel):
    question: str


class RAGResponse(BaseModel):
    answer: str
