from enum import StrEnum


class Prompt(StrEnum):
    RAG_SYSTEM_PROMPT = """
        You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.
        
        Context: 
        <<{context}>>
        
        Previous user messages:
        <<{messages}>>
    """

    RAG_REQUEST_PROMPT = """
        Given a list of messages, create a phrase that will be used in a search in a RAG system.
        Extract the entity that user is asking about in the last message and use it in a phrase
        that will be used for RAG.
        
        All messages:
        <<{messages}>>
    """
