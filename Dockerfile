FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN python app/utils/crawl_data.py

EXPOSE 8000
EXPOSE 6379
EXPOSE 8501

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "app.main"]