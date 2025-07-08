
Este projeto utiliza Python e FastAPI para consumir e disponibilizar dados públicos da API oficial do Star Wars (SWAPI).

Necessário poetry para executar poetry, python, docker


poetry run uvicorn src.starwars_api.main:app --host 0.0.0.0 --port 8000 --reload


## Sorting 

```
GET /films/?sort_by=title&order=desc
```


## JWT

Utilize o comando para gerar uma chave para utilizar com o seu secret key

```
openssl rand -hex 64
``` 

## .env

Variaveis de ambiente são 

```
REDIS_URL="redis://redis:6379"
JWT_SECRET_KEY=73d05dcc678b110cdcca8f9f2c09316629615527b9e30e93a4b25c45a4d291fa222268248acc68fea40c8362d8aab8d481daa958de71d8b4e6039bccd9da6a4d
```

Não estou colocando ele no gitignore por não ter nenhum dado sensível e para executar os testes

## Redis & Docker

Estou utilizando cache para evitar vários requests e para trocar a resposta em url pelo nome 

Temos que subir um container docker para utilizar o redis

```
docker compose up -d
```