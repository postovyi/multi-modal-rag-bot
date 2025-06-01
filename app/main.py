import uvicorn
from fastapi import FastAPI

from app.api.endpoints import main_router
from app.config import settings

app = FastAPI()
app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        loop='asyncio',
    )
