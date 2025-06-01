from .base import BaseConfig


class StreamlitConfig(BaseConfig):
    STREAMLIT_BACKEND_HOST: str = 'app'
    STREAMLIT_BACKEND_PORT: int = 8000
