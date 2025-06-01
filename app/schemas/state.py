from typing import Any

from langgraph.graph import MessagesState


class RAGState(MessagesState):
    relevant_docs: list[Any]
    last_recorded_question: str
    evaluation_metrics: list
