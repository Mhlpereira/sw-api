FROM python:3.10-slim

WORKDIR /app

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"


RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --only=main --no-root

COPY . .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=300s --start-period=240s --retries=3 \
  CMD curl -f http://0.0.0.0:8080/health || exit 1

CMD ["uvicorn", "starwars_api.main:app", "--host", "0.0.0.0", "--port", "8080"]