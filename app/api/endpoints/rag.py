from fastapi import APIRouter

from app.schemas import Question, RAGResponse
from app.services import rag_service

rag_router = APIRouter(prefix='/rag')


@rag_router.post('/', response_model=RAGResponse)
async def rag(data: Question) -> RAGResponse:
    return await rag_service.ainvoke(data)
