
# Star Wars API Gateway

Uma API construída com FastAPI, que consome dados da API pública do swapi.info. O sistema utiliza Redis para cache eficiente, reduzindo a latência e a carga sobre a API original. Implementa resolução inteligente de URLs, convertendo links brutos em nomes legíveis e informativos.

O deploy foi realizado na AWS utilizando Lambda Functions com API Gateway. O Redis está hospedado em uma instância EC2 dedicada, separando a camada de cache para melhor desempenho e controle.

A aplicação utiliza Mangum como adapter para executar FastAPI em ambiente serverless AWS Lambda. O sistema implementa controle de concorrência com semáforos e retry automático com Tenacity para garantir robustez na integração com APIs externas.

## 🧭 Como Usar
Para começar a utilizar a API, siga os passos abaixo:

### 1. 🔥 Faça o Warm-Up do Cache (opcional)
Antes de realizar consultas, é recomendável popular o cache com todos os dados da SWAPI para garantir desempenho máximo e respostas legíveis com nomes em vez de URLs.

```bash
curl -X POST https://qy5sfbks3c.execute-api.us-east-1.amazonaws.com/deploy/swapi-function/warm-cache
```

Esse processo:
- Pré-carrega os dados da API pública no Redis
- Resolve automaticamente as URLs em nomes legíveis
- Reduz significativamente a latência das próximas requisições

### 2. 🔐 Gere um Token de Autenticação (JWT)
A maioria dos endpoints requer autenticação. Para isso, gere um token JWT:

```bash
curl -X POST https://qy5sfbks3c.execute-api.us-east-1.amazonaws.com/deploy/swapi-function/auth
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. 📡 Faça Requisições Autenticadas
Agora que você tem um token JWT, use-o no header Authorization das suas requisições:

```bash
curl -H "Authorization: Bearer <seu_token>" https://qy5sfbks3c.execute-api.us-east-1.amazonaws.com/deploy/swapi-function/swapi/people
```

### 4. 🔄 Resultado com Resolução de Nomes
Graças ao warm-up e à lógica de cache inteligente, a resposta da API já virá com nomes resolvidos:

```json
{
  "name": "Luke Skywalker",
  "homeworld": "Tatooine",
  "films": ["A New Hope"]
}
```

## 🌐 Acesso via API Gateway

**Base URL**: `https://qy5sfbks3c.execute-api.us-east-1.amazonaws.com/deploy/swapi-function`

A API está disponível através do AWS API Gateway que invoca uma Lambda Function.

## 🏗️ Arquitetura

- **Frontend**: AWS API Gateway
- **Backend**: FastAPI + Mangum (Python 3.10+)
- **Compute**: AWS Lambda Function
- **Cache**: Redis (EC2 instance)
- **Fonte de Dados**: SWAPI Pública (swapi.info)

### Componentes Técnicos

- **Mangum**: Adapter que permite executar aplicações FastAPI em AWS Lambda
- **Semáforo**: Controla concorrência para evitar sobrecarga na API externa
- **Tenacity**: Implementa retry automático com backoff exponencial para requests HTTP

## 🚀 Funcionalidades Principais

### ✅ Consumo da API Pública SWAPI
- Integração completa com a API oficial do Star Wars
- Dados em tempo real de pessoas, filmes, naves, veículos, espécies e planetas
- Sistema de fallback para garantir disponibilidade

### ✅ Sistema de Cache Inteligente
- **Redis** hospedado em EC2 na AWS para performance máxima
- Cache automático de todas as consultas
- Resolução de URLs para nomes (ex: `https://swapi.info/api/planets/1` → `"Tatooine"`)
- TTL configurável para otimizar recursos

### ✅ Autenticação JWT
- Tokens seguros com expiração configurável
- Proteção de endpoints sensíveis
- Middleware de autenticação robusto

## 🔧 Configuração Local (Desenvolvimento)

### Pré-requisitos
- **Python 3.10+**
- **Poetry** (gerenciamento de dependências)
- **Docker** (para Redis local)

### Instalação
```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd starwars_api

# 2. Instale dependências
poetry install

# 3. Configure variáveis de ambiente
cp .env.example .env

# 4. Inicie Redis local
docker compose up -d

# 5. Execute a aplicação
poetry run uvicorn src.starwars_api.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔐 Autenticação

### 1. Gerar Bearer Token

Faça uma requisição POST para obter o token JWT:

```bash
curl -X POST https://qy5sfbks3c.execute-api.us-east-1.amazonaws.com/deploy/swapi-function/auth
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Usar o Token

Inclua o token no header `Authorization` de todas as requisições para endpoints protegidos:

```bash
curl -H "Authorization: Bearer <seu_token>" https://qy5sfbks3c.execute-api.us-east-1.amazonaws.com/deploy/swapi-function/swapi/people
```

## 🔗 Endpoints Disponíveis

### 🏥 Monitoramento
- `GET /health` - Health check da aplicação

### 🔐 Autenticação
- `POST /auth` - Gerar token JWT
- `POST /warm-cache` - Popular cache Redis (recomendado após deploy)

### 📊 SWAPI Endpoints (requerem autenticação)

#### Pessoas
- `GET /swapi/people` - Listar todas as pessoas
- `GET /swapi/people/{id}` - Obter pessoa específica

#### Filmes
- `GET /swapi/films` - Listar todos os filmes
- `GET /swapi/films/{id}` - Obter filme específico

#### Naves Estelares
- `GET /swapi/starships` - Listar todas as naves
- `GET /swapi/starships/{id}` - Obter nave específica

#### Veículos
- `GET /swapi/vehicles` - Listar todos os veículos
- `GET /swapi/vehicles/{id}` - Obter veículo específico

#### Espécies
- `GET /swapi/species` - Listar todas as espécies
- `GET /swapi/species/{id}` - Obter espécie específica

#### Planetas
- `GET /swapi/planets` - Listar todos os planetas
- `GET /swapi/planets/{id}` - Obter planeta específico

## 🔍 Filtros e Ordenação

### Filtros Disponíveis

Todos os endpoints suportam filtros específicos para consultas precisas:

**Exemplos:**
```bash
# Filtrar pessoas por nome
GET /swapi/people?name=Luke

# Filtrar filmes por diretor
GET /swapi/films?director=Lucas

# Filtrar naves por classe
GET /swapi/starships?starship_class=Starfighter

# Múltiplos filtros
GET /swapi/people?name=Luke&eye_color=blue
```

### Ordenação

Todos os endpoints suportam ordenação por qualquer campo:

```bash
# Ordenar filmes por título (crescente)
GET /swapi/films?order=asc&order_by=title

# Ordenar pessoas por altura (decrescente)
GET /swapi/people?order=desc&order_by=height

# Ordenar planetas por população
GET /swapi/planets?order=desc&order_by=population
```

## 💾 Sistema de Cache Redis

### Estratégia de Cache

O sistema utiliza **Redis** hospedado em EC2 na AWS para otimizar performance:

#### 🚀 Warm-up do Cache (Recomendado)
```bash
# Popular cache com todos os dados da SWAPI
curl -X POST https://qy5sfbks3c.execute-api.us-east-1.amazonaws.com/deploy/swapi-function/warm-cache
```

**Benefícios:**
- Cache pré-populado com todos os dados
- Resolução prévia de URLs para nomes
- Consultas subsequentes instantâneas
- Redução de latência significativa

#### 🔄 Cache Automático
Se não usar o warm-up, o cache é populado automaticamente:
- Primeira consulta: busca da SWAPI pública + cache
- Consultas seguintes: resposta instantânea do cache
- URLs são resolvidas e cacheadas automaticamente

### Resolução de URLs para Nomes

O sistema converte automaticamente URLs da SWAPI para nomes legíveis:

```json
// Antes
{
  "name": "Luke Skywalker",
  "homeworld": "https://swapi.info/api/planets/1",
  "films": ["https://swapi.info/api/films/1"]
}

// Depois
{
  "name": "Luke Skywalker",
  "homeworld": "Tatooine",
  "films": ["A New Hope"]
}
```

## 🏥 Health Check

Monitore a saúde da aplicação:

```bash
GET /health
```

**Resposta:**
```json
{
  "status": "ready"
}
```

### Fluxo de Dados

```
Cliente → AWS API Gateway → Lambda Function → Redis (EC2)
                                ↓
                           SWAPI.info
```

1. **Cliente** faz requisição via AWS API Gateway
2. **API Gateway** roteia para Lambda Function
3. **Lambda Function** (FastAPI + Mangum) verifica cache no Redis
4. Se não cached: busca na **SWAPI pública** com retry automático
5. **Redis** armazena resultado para consultas futuras
6. **Resposta** retorna via API Gateway

## ⚙️ Componentes Técnicos

### Mangum
Adapter que permite executar aplicações ASGI (FastAPI) em AWS Lambda Functions, convertendo eventos Lambda para requisições HTTP.

### Semáforo (asyncio.Semaphore)
Controla a concorrência limitando o número de requisições simultâneas para a API externa, evitando sobrecarga e rate limits.

### Tenacity
Implementa retry automático com backoff exponencial para requisições HTTP que falham, garantindo maior robustez na integração com APIs externas.

## ⚙️ Configuração de Ambiente

### Variáveis de Ambiente

```bash
# Redis Local
REDIS_URL="redis://localhost:6379"

# JWT Secret Key
JWT_SECRET_KEY=your_secure_secret_key_here

# SWAPI Base URL
SWAPI_BASE_URL="https://swapi.info/api"
```

## 🐳 Desenvolvimento Local

### Executar com Docker:
```bash
# Iniciar Redis local
docker compose up -d

# Verificar status
docker compose ps

# Executar aplicação
poetry run uvicorn src.starwars_api.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🧪 Testes

### Executar todos os testes:
```bash
poetry run pytest
```

### Testes específicos:
```bash
# Testes de rotas
poetry run pytest tests/test_routes.py -v

# Testes de serviços
poetry run pytest tests/test_swapi_service.py -v

# Testes de autenticação
poetry run pytest tests/test_auth_service.py -v
```

## 📚 Documentação

### Swagger UI
```
https://qy5sfbks3c.execute-api.us-east-1.amazonaws.com/deploy/swapi-function/docs
```

### Desenvolvimento Local
```
http://localhost:8000/docs
```

## 🛠️ Estrutura do Projeto

```
starwars_api/
├── src/starwars_api/
│   ├── main.py                 # Aplicação FastAPI principal
│   ├── cache/                  # Sistema de cache Redis
│   │   ├── cache.py           # Interface do cache
│   │   ├── cache_instance.py  # Instância Redis
│   │   └── warmup_service.py  # Serviço de warm-up
│   ├── routes/                 # Rotas da API
│   │   ├── auth_router.py     # Endpoints de autenticação
│   │   ├── swapi_router.py    # Endpoints SWAPI
│   │   └── dto/               # Data Transfer Objects
│   ├── services/               # Lógica de negócio
│   │   ├── auth_service.py    # Serviço de autenticação
│   │   └── swapi_service.py   # Serviço SWAPI
│   ├── util/                   # Utilitários
│   │   ├── naming.py          # Resolução de nomes
│   │   ├── sorting.py         # Ordenação
│   │   └── resolve_name_fields.py # Resolução de campos
│   └── enums/                  # Enumerações
│       └── order_enum.py      # Enum de ordenação
├── tests/                      # Testes automatizados
├── docker-compose.yml          # Configuração Redis local
├── Dockerfile                  # Container da aplicação
└── pyproject.toml             # Configuração Poetry
```
