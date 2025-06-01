# SoftServe test task

A Retrieval-Augmented Generation (RAG) bot application that scrapes The Batch articles. 
GenAI test assignment for SofServe.

## Environment variables:
- OPENAI_API_KEY: OpenAI API token
- LANGCHAIN_API_KEY: LangSmith API token for tracing

To run the chat interface, use:
```bash
docker-compose up --build
```
Then access the chat at: 'http://localhost:8501' (or 'http://0.0.0.0:8501' for Linux users)

The app starts with scraping articles from 'https://www.deeplearning.ai/the-batch/' using **scrapy**.
The app uses N-level architecture (a database can be easily added to save users' interactions).

## Main service
The core service is a RAGService that uses LangGraph workflow.
This framework was chosen because it is a part of a LangChain ecosystem and can be integrated with
LangSmith to trace LLM calls and responses. I also used LangSmith datasets to create test cases for
system evaluation. The core workflow can also be expanded to use more agent-oriented concepts.

## Vectorstore
Chroma was chosen to store embeddings. It is the simplest vectorstore to use and can be run as
a separate docker container.

## Evaluation
DeepEval was used for system evaluation. I integrated it with pytest, so it can be the part of the CI/CD
workflow. I used ContextualRelevancyMetric and FaithfulnessMetric to evaluate RAG. The main reason to choose
these 2 metrics was the absense of a mandatory 'expected_output' field. Expected output may be undefined
in such systems because of the size of retrieved docs. ContextualRelevancyMetric allows evaluating how much
irrelevant information the system yields based on retrieved context. FaithfulnessMetric allows to see if LLM
generated the faithful answer based on the given context.

## GUI
Simple chat GUI using Streamlit.

## Other
Using REST API created with FastAPI to interact with the system. Using Pydantic schemas for data validation.
Using separate configs for different parts of the system. Using StrEnum to define prompts.

## Video
Demonstration of the program is available at https://www.dropbox.com/scl/fi/gta7taihkjpkpx5kab0ap/2025-06-01-20-44-17.mkv?rlkey=iu7odzfqavojnf14eiy9l0dpa&st=kxck9hgu&dl=0