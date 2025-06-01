from .base import BaseConfig


class AIConfig(BaseConfig):
    OPENAI_API_KEY: str = ''
    OPENAI_MODEL: str = 'gpt-4.1-mini'
    EMBEDDING_MODEL: str = 'text-embedding-3-large'
