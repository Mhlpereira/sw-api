
# Star Wars API

Este projeto utiliza Python e FastAPI para consumir e disponibilizar dados públicos da API oficial do Star Wars (SWAPI) com funcionalidades de cache, autenticação JWT e resolução de URLs para nomes.

## 🚀 Pré-requisitos

- **Python 3.10+**
- **Poetry** (para gerenciamento de dependências)
- **Docker** (para Redis)

## 📦 Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd starwars_api
```

2. **Instale as dependências:**
```bash
poetry install
```

3. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env  # ou crie o arquivo .env
```

4. **Inicie o Redis:**
```bash
docker compose up -d
```

## 🏃‍♂️ Como Executar

### Desenvolvimento (com reload automático):
```bash
poetry run uvicorn src.starwars_api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Produção:
```bash
poetry run uvicorn src.starwars_api.main:app --host 0.0.0.0 --port 8000
```

### Executar via Python:
```bash
poetry run python src/starwars_api/main.py
```

## 🔐 Autenticação

### 1. Gerar Bearer Token

Faça uma requisição POST para obter o token JWT:

```bash
curl -X POST http://localhost:8000/auth/auth
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
curl -H "Authorization: Bearer <seu_token>" http://localhost:8000/api/v1/swapi/people
```

## 🔗 Endpoints Principais

### Autenticação
- `POST /auth/auth` - Gerar token JWT
- `POST /auth/warm-cache` - Aquecer cache (opcional)

### SWAPI Endpoints (requerem autenticação)
- `GET /api/v1/swapi/people` - Listar pessoas
- `GET /api/v1/swapi/people/{id}` - Obter pessoa específica
- `GET /api/v1/swapi/films` - Listar filmes
- `GET /api/v1/swapi/films/{id}` - Obter filme específico
- `GET /api/v1/swapi/starships` - Listar naves
- `GET /api/v1/swapi/starships/{id}` - Obter nave específica
- `GET /api/v1/swapi/vehicles` - Listar veículos
- `GET /api/v1/swapi/vehicles/{id}` - Obter veículo específico
- `GET /api/v1/swapi/species` - Listar espécies
- `GET /api/v1/swapi/species/{id}` - Obter espécie específica
- `GET /api/v1/swapi/planets` - Listar planetas
- `GET /api/v1/swapi/planets/{id}` - Obter planeta específico

## 🔍 Filtros e Ordenação

### Filtros Disponíveis

Cada endpoint suporta filtros específicos:

**Pessoas:**
```bash
GET /api/v1/swapi/people?name=Luke&homeworld=Tatooine
```

**Filmes:**
```bash
GET /api/v1/swapi/films?title=Hope&director=Lucas
```

### Ordenação

Todos os endpoints suportam ordenação:

```bash
# Crescente (padrão)
GET /api/v1/swapi/films?sort_by=title&order=asc

# Decrescente
GET /api/v1/swapi/films?sort_by=title&order=desc
```

**Campos ordenáveis:**
- `name` (pessoas, espécies, planetas, etc.)
- `title` (filmes)
- `height` (pessoas)
- `release_date` (filmes)
- E muitos outros...

## 💾 Sistema de Cache

O projeto utiliza **Redis** para cache inteligente:

### Funcionalidades:
- ✅ Cache automático de todas as requisições
- ✅ Resolução de URLs para nomes (ex: `https://swapi.info/api/planets/1` → `"Tatooine"`)
- ✅ TTL de 1 hora para todos os dados
- ✅ Warm-up manual do cache

### Warm-up do Cache:
```bash
curl -X POST http://localhost:8000/auth/warm-cache
```

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# Redis (desenvolvimento local)
REDIS_URL="redis://localhost:6379"

# Redis (Docker Compose)
REDIS_URL="redis://redis:6379"

# JWT Secret Key
JWT_SECRET_KEY=73d05dcc678b110cdcca8f9f2c09316629615527b9e30e93a4b25c45a4d291fa222268248acc68fea40c8362d8aab8d481daa958de71d8b4e6039bccd9da6a4d
```

### Gerar Nova JWT Secret Key:
```bash
openssl rand -hex 64
```

## 🐳 Docker

### Redis via Docker Compose:
```bash
# Iniciar Redis
docker compose up -d

# Verificar status
docker compose ps

# Parar Redis
docker compose down
```

## 🧪 Testes

### Executar todos os testes:
```bash
poetry run pytest
```

### Executar testes específicos:
```bash
# Testes de rota
poetry run pytest tests/test_routes.py -v

# Testes de utilitários
poetry run pytest tests/test_utils.py -v

# Testes que funcionam 100%
poetry run pytest tests/test_working.py -v
```

### Executar com cobertura:
```bash
poetry run pytest --cov=src/starwars_api
```

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🌟 Funcionalidades Especiais

### 1. Resolução Automática de URLs
URLs da SWAPI são automaticamente convertidas para nomes legíveis:

**Antes:**
```json
{
  "name": "Luke Skywalker",
  "homeworld": "https://swapi.info/api/planets/1",
  "films": ["https://swapi.info/api/films/1"]
}
```

**Depois:**
```json
{
  "name": "Luke Skywalker",
  "homeworld": "Tatooine",
  "films": ["A New Hope"]
}
```

### 2. Cache Inteligente
- Dados ficam em cache por 1 hora
- URLs são cacheadas separadamente dos nomes
- Sistema de fallback em caso de falha no cache

### 3. Ordenação Numérica Inteligente
O sistema detecta automaticamente campos numéricos e os ordena corretamente:
- `"height": "172"` é tratado como número 172
- Mistura de números e strings funciona perfeitamente

## 🛠️ Estrutura do Projeto

```
starwars_api/
├── src/starwars_api/
│   ├── cache/          # Sistema de cache Redis
│   ├── enums/          # Enumerações (Order)
│   ├── routes/         # Rotas da API e DTOs
│   ├── services/       # Lógica de negócio
│   └── util/           # Utilitários (sorting, naming, etc.)
├── tests/              # Testes automatizados
├── docker-compose.yml  # Configuração do Redis
├── pyproject.toml      # Configuração do Poetry
└── README.md          # Este arquivo
```

## ❓ Solução de Problemas

### Redis não conecta:
```bash
# Verificar se Redis está rodando
docker compose ps

# Verificar logs
docker compose logs redis

# Reiniciar Redis
docker compose restart redis
```

### Erro de autenticação:
1. Gere um novo token via `POST /auth/auth`
2. Verifique se o header está correto: `Authorization: Bearer <token>`
3. Tokens expiram em 1 hora

### Cache não funciona:
1. Verifique se Redis está rodando
2. Confirme a variável `REDIS_URL` no `.env`
3. Use `POST /auth/warm-cache` para popular o cache

## 📝 Notas

- O arquivo `.env` não está no `.gitignore` propositalmente para facilitar os testes
- A JWT Secret Key fornecida é apenas para desenvolvimento
- Para produção, gere uma nova secret key e configure adequadamente o Redis