FROM python:3.10-slim

WORKDIR /app
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/src"

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry lock && \
    poetry install --only=main --no-root

COPY ./src ./src

EXPOSE 8000

CMD ["uvicorn", "starwars_api.main:app", "--host", "0.0.0.0", "--port", "8000"]