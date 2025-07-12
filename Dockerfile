FROM public.ecr.aws/lambda/python:3.10

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --only=main --no-interaction --no-ansi

RUN pip install mangum

COPY src/ ./src/

CMD ["src.starwars_api.main.handler"]