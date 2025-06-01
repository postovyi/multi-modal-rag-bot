import json
from collections.abc import Sequence
from typing import Any

import chromadb
import loguru
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.retrievers import BaseRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langsmith import traceable

from app.config import settings
from app.enums.prompts import Prompt
from app.schemas import Question, RAGResponse, RAGState


class RAGService:
    def __init__(self) -> None:
        self.builder = StateGraph(RAGState)
        self.builder.add_node(self.reply_node.__name__, self.reply_node)
        self.builder.add_edge(START, self.reply_node.__name__)
        self.builder.add_edge(self.reply_node.__name__, END)
        self.config = {'configurable': {'thread_id': 'test_conversation'}}  # Will update this logic
        self.memory = MemorySaver()
        self.workflow = self.builder.compile(checkpointer=self.memory)
        self.docs = []
        self.retriever = None
        self.embeddings = OpenAIEmbeddings(
            model=settings.ai.EMBEDDING_MODEL,
            api_key=settings.ai.OPENAI_API_KEY,
        )
        self.llm = ChatOpenAI(
            model=settings.ai.OPENAI_MODEL,
            temperature=0,
            api_key=settings.ai.OPENAI_API_KEY,
        )
        self.data_path = 'app/utils/output_programmatic.json'
        self.chroma = Chroma(
            collection_name=settings.chroma.COLLECTION_NAME,
            client=chromadb.HttpClient(
                host=settings.chroma.CHROMA_DB_HOST, port=settings.chroma.CHROMA_DB_PORT
            ),
            embedding_function=self.embeddings,
        )

    def get_docs(self) -> None:
        if not self.docs:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                docs = json.load(f)
            for d in docs:
                self.docs.append(Document(page_content=d['content'], metadata={'url': d['url']}))

    def get_retriever(self) -> BaseRetriever:
        self.get_docs()
        if not self.retriever:
            self.chroma.add_documents(self.docs, ids=[d.metadata['url'] for d in self.docs])
            self.retriever = self.chroma.as_retriever(search_kwargs={'k': 5})
        return self.retriever

    @traceable
    async def reply_node(self, state: RAGState) -> dict[str, Any]:
        loguru.logger.info(state['messages'])
        question = await self.create_rag_request(state['messages'])
        relevant_docs = await self.get_retriever().ainvoke(question)
        response = await self.llm.ainvoke(
            [
                SystemMessage(
                    content=Prompt.RAG_SYSTEM_PROMPT.format(
                        context=relevant_docs, messages=state['messages']
                    )
                )
            ]
        )
        return {
            'messages': [AIMessage(content=response.content)],
            'relevant_docs': relevant_docs,
            'last_recorded_question': question,
        }

    async def create_rag_request(self, messages: Sequence[BaseMessage]) -> str:
        response = await self.llm.with_structured_output(Question).ainvoke(
            [HumanMessage(content=Prompt.RAG_REQUEST_PROMPT.format(messages=messages))]
        )
        return response.question

    async def ainvoke(self, question: Question) -> RAGResponse:
        result = await self.workflow.ainvoke(
            {'messages': [HumanMessage(question.question)]}, config=self.config
        )
        return RAGResponse(answer=result['messages'][-1].content)


rag_service = RAGService()
