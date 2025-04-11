FROM python:3.13-alpine

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --extra speed --extra sqlite

COPY . .

CMD ["uv", "run", "main.py"]
