from .ai import AIConfig
from .base import BaseConfig
from .chroma import ChromaConfig
from .streamlit import StreamlitConfig


class Settings(BaseConfig):
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    DEBUG: bool = True

    chroma: ChromaConfig = ChromaConfig()
    ai: AIConfig = AIConfig()
    streamlit: StreamlitConfig = StreamlitConfig()


settings = Settings()
