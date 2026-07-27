FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY . .

RUN uv add openai minsearch requests python-dotenv pydantic-ai logfire 
RUN uv add "dlt[duckdb]"
RUN uv add "pydantic-ai-slim[groq]"

CMD ["uv", "run", "python", "main.py"]
