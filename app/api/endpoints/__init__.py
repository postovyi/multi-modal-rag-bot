from fastapi import APIRouter

from .rag import rag_router

main_router = APIRouter(prefix='/api')
main_router.include_router(rag_router)
