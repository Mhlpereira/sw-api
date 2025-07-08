FROM python:3.9-slim as builder

WORKDIR /app
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root

FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY ./app ./app

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]