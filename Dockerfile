FROM public.ecr.aws/lambda/python:3.10

WORKDIR /var/task

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["starwars_api.main.handler"]