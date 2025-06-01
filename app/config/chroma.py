from .base import BaseConfig


class ChromaConfig(BaseConfig):
    CHROMA_DB_HOST: str = '0.0.0.0'
    CHROMA_DB_PORT: int = 6379
    COLLECTION_NAME: str = 'the_batch_docs'
