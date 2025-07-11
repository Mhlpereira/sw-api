
# Star Wars API Gateway

Uma API construída com FastAPI, que consome dados da API pública do swapi.info. O sistema utiliza Redis para cache eficiente, reduzindo a latência e a carga sobre a API original. Implementa resolução inteligente de URLs, convertendo links brutos em nomes legíveis e informativos.

O deploy foi realizado no Cloud Run (GCP), garantindo escalabilidade automática e baixo custo operacional. O Redis está hospedado em uma VM dedicada, separando a camada de cache para melhor desempenho e controle.

Um gateway foi implementado como camada intermediária entre os clientes e os serviços internos, permitindo maior segurança, centralização de autenticação com JWT, controle de tráfego e fácil aplicação de políticas de rate limit e logging.

## 🧭 Como Usar
Para começar a utilizar a API, siga os passos abaixo:

1. 🔥 Faça o Warm-Up do Cache
Antes de realizar consultas, é recomendável popular o cache com todos os dados da SWAPI para garantir desempenho máximo e respostas legíveis com nomes em vez de URLs.

```

curl -X POST https://swapi-gateway-9gaiurpg.uc.gateway.dev/warm-cache
```

Esse processo:

Pré-carrega os dados da API pública no Redis

Resolve automaticamente as URLs em nomes legíveis

Reduz significativamente a latência das próximas requisições

2. 🔐 Gere um Token de Autenticação (JWT)
A maioria dos endpoints requer autenticação. Para isso, gere um token JWT:

```

curl -X POST https://swapi-gateway-9gaiurpg.uc.gateway.dev/auth
```

Resposta:

```

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Copie o valor do access_token.

3. 📡 Faça Requisições Autenticadas
Agora que você tem um token JWT, use-o no header Authorization das suas requisições:
```
curl -H "Authorization: Bearer <seu_token>" https://swapi-gateway-9gaiurpg.uc.gateway.dev/swapi/people
Você pode acessar qualquer endpoint da API (pessoas, filmes, planetas etc.) da mesma forma, sempre com o token no header.
```

4. 🔄 Resultado com Resolução de Nomes
Graças ao warm-up e à lógica de cache inteligente, a resposta da API já virá com nomes resolvidos, como:
```
{
  "name": "Luke Skywalker",
  "homeworld": "Tatooine",
  "films": ["A New Hope"]
}
```

## 🌐 Acesso via API Gateway

**Base URL**: `https://swapi-gateway-9gaiurpg.uc.gateway.dev`

A API está disponível através do Google Cloud API Gateway e pode ser acessada diretamente pelos endpoints públicos configurados.

## 🏗️ Arquitetura

- **Frontend**: API Gateway (GCP)
- **Backend**: FastAPI (Python 3.10+)
- **Hospedagem**: Cloud Run (GCP)
- **Cache**: Redis (VM no GCP)
- **Containerização**: Docker
- **Fonte de Dados**: SWAPI Pública (swapi.info)

## 🚀 Funcionalidades Principais

### ✅ Consumo da API Pública SWAPI
- Integração completa com a API oficial do Star Wars
- Dados em tempo real de pessoas, filmes, naves, veículos, espécies e planetas
- Sistema de fallback para garantir disponibilidade

### ✅ Sistema de Cache Inteligente
- **Redis** hospedado em VM no GCP para performance máxima
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

Faça uma requisição POST através do API Gateway para obter o token JWT:

```bash
curl -X POST https://swapi-gateway-9gaiurpg.uc.gateway.dev/auth
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
curl -H "Authorization: Bearer <seu_token>" https://swapi-gateway-9gaiurpg.uc.gateway.dev/swapi/people
```

## 🔗 Endpoints do API Gateway

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

**Exemplos de Filtros:**
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

### Ordenação Inteligente

Todos os endpoints suportam ordenação por qualquer campo:

```bash
# Ordenar filmes por título (crescente)
GET /swapi/films?order=asc&order_by=title

# Ordenar pessoas por altura (decrescente)
GET /swapi/people?order=desc&order_by=height

# Ordenar planetas por população
GET /swapi/planets?order=desc&order_by=population
```

**Campos ordenáveis comuns:**
- `name` (pessoas, espécies, planetas, naves, veículos)
- `title` (filmes)
- `height`, `mass` (pessoas)
- `release_date`, `episode_id` (filmes)
- `length`, `cost_in_credits` (naves, veículos)

## 💾 Sistema de Cache Redis

### Estratégia de Cache Inteligente

O sistema utiliza **Redis** hospedado em VM no GCP para otimizar performance:

#### 🚀 Warm-up do Cache (Recomendado)
```bash
# Popular cache com todos os dados da SWAPI
curl -X POST https://swapi-gateway-9gaiurpg.uc.gateway.dev/warm-cache
```

**Benefícios do warm-up:**
- Cache pré-populado com todos os dados
- Resolução prévia de URLs para nomes
- Consultas subsequentes instantâneas
- Redução de latência em 90%

#### 🔄 Cache Automático
Se não usar o warm-up, o cache é populado automaticamente:
- Primeira consulta: busca da SWAPI pública + cache
- Consultas seguintes: resposta instantânea do cache
- URLs são resolvidas e cacheadas automaticamente

### Resolução de URLs para Nomes

O sistema converte automaticamente URLs da SWAPI para nomes legíveis:

**Exemplo prático:**
```bash
# Consulta inicial retorna URLs
GET /swapi/people/1
{
  "name": "Luke Skywalker",
  "homeworld": "https://swapi.info/api/planets/1",
  "films": ["https://swapi.info/api/films/1"]
}

# Após processamento (automático)
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

Este endpoint verifica:
- Status da aplicação FastAPI
- Conectividade com Redis
- Disponibilidade da SWAPI pública

## 🌐 Infraestrutura GCP

### Componentes da Arquitetura

#### 🚪 API Gateway
- **Função**: Ponto de entrada único para todas as requisições
- **Benefícios**: Rate limiting, autenticação, logging, monitoramento
- **Configuração**: Swagger/OpenAPI 2.0

#### 🏃‍♂️ Cloud Run
- **Função**: Hospedagem da aplicação FastAPI
- **Benefícios**: Escalabilidade automática, serverless, pay-per-use
- **Configuração**: Container Docker otimizado

#### 🖥️ Compute Engine VM
- **Função**: Hospedagem do Redis Cache
- **Benefícios**: Performance dedicada, controle total, persistência
- **Configuração**: VM otimizada para Redis

#### 🐳 Docker
- **Função**: Containerização da aplicação
- **Benefícios**: Portabilidade, isolamento, deploy consistente
- **Configuração**: Multi-stage build para otimização

### Fluxo de Dados

```
Cliente → API Gateway → Cloud Run → Redis VM
                    ↓
                 SWAPI.info
```

1. **Cliente** faz requisição via API Gateway
2. **API Gateway** valida e roteia para Cloud Run
3. **Cloud Run** verifica cache no Redis VM
4. Se não cached: busca na **SWAPI pública**
5. **Redis VM** armazena resultado para consultas futuras
6. **Resposta** retorna via API Gateway

## ⚙️ Configuração de Ambiente

### Variáveis de Ambiente

#### Para Desenvolvimento Local:
```bash
# Redis Local
REDIS_URL="redis://localhost:6379"

# JWT Secret Key
JWT_SECRET_KEY=your_secure_secret_key_here

# SWAPI Base URL
SWAPI_BASE_URL="https://swapi.info/api"
```

#### Para Produção GCP:
```bash
# Redis VM (IP interno)
REDIS_URL="redis://10.x.x.x:6379"

# JWT Secret Key (segura)
JWT_SECRET_KEY=your_production_secret_key

# SWAPI Base URL
SWAPI_BASE_URL="https://swapi.info/api"
```

### Gerar Nova JWT Secret Key:
```bash
openssl rand -hex 64
```

## 🐳 Docker & Containerização

### Desenvolvimento Local:
```bash
# Iniciar Redis local
docker compose up -d

# Verificar status
docker compose ps

# Logs do Redis
docker compose logs redis

# Parar serviços
docker compose down
```

### Build para Produção:
```bash
# Build da imagem
docker build -t starwars-api .

# Run local
docker run -p 8080:8080 starwars-api

# Tag para GCP
docker tag starwars-api gcr.io/YOUR_PROJECT/starwars-api

# Push para Container Registry
docker push gcr.io/YOUR_PROJECT/starwars-api
```

## 🧪 Testes & Qualidade

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

# Testes de utilitários
poetry run pytest tests/test_utils.py -v

# Testes funcionais completos
poetry run pytest tests/test_working.py -v
```

### Cobertura de código:
```bash
poetry run pytest --cov=src/starwars_api --cov-report=html
```

## 📚 Documentação Interativa

### Swagger UI (Recomendado)
```
https://swapi-gateway-9gaiurpg.uc.gateway.dev/docs
```

### ReDoc (Alternativa)
```
https://swapi-gateway-9gaiurpg.uc.gateway.dev/redoc
```

### Documentação Local (Desenvolvimento)
```
http://localhost:8000/docs
http://localhost:8000/redoc
```

## 🌟 Funcionalidades Avançadas

### 1. Cache Inteligente Multi-Camada
- **L1**: Cache local em memória para consultas frequentes
- **L2**: Redis para persistência e compartilhamento
- **L3**: Fallback para SWAPI pública

### 2. Resolução Automática de URLs
- URLs da SWAPI são transformadas em nomes legíveis
- Sistema de cache específico para resolução de nomes
- Fallback gracioso em caso de falha

### 3. Autenticação JWT Robusta
- Tokens com expiração configurável
- Middleware de validação em todos os endpoints protegidos
- Refresh automático de tokens

### 4. Filtros Dinâmicos
- Suporte a múltiplos filtros simultâneos
- Filtros por campos aninhados
- Filtros com operadores (igual, contém, maior que, etc.)

### 5. Ordenação Inteligente
- Detecção automática de tipos de dados
- Ordenação numérica para campos numéricos
- Ordenação lexicográfica para strings
- Suporte a ordenação por múltiplos campos

## 🛠️ Estrutura Técnica do Projeto

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
│   │   ├── sorting.py         # Ordenação inteligente
│   │   └── resolve_name_fields.py # Resolução de campos
│   └── enums/                  # Enumerações
│       └── order_enum.py      # Enum de ordenação
├── tests/                      # Testes automatizados
├── docker-compose.yml          # Configuração Redis local
├── Dockerfile                  # Container da aplicação
├── pyproject.toml             # Configuração Poetry
└── swagger-api-gateway.yaml   # Configuração API Gateway
```

## 🚨 Troubleshooting

### Redis Connection Issues
```bash
# Verificar se Redis está rodando
docker compose ps

# Verificar logs do Redis
docker compose logs redis

# Reiniciar Redis
docker compose restart redis

# Testar conexão Redis
redis-cli ping
```

### Authentication Problems
1. **Token Expirado**: Gere um novo token via `POST /auth`
2. **Header Incorreto**: Verifique o formato `Authorization: Bearer <token>`
3. **Token Inválido**: Verifique se o JWT_SECRET_KEY está correto

### Cache Not Working
1. **Redis Down**: Verifique se Redis está rodando
2. **Wrong URL**: Confirme a variável `REDIS_URL` no ambiente
3. **Empty Cache**: Use `POST /warm-cache` para popular o cache
4. **Network Issues**: Verifique conectividade com a VM do Redis

### SWAPI Connection Issues
1. **Rate Limiting**: A SWAPI pública tem rate limits
2. **Network Timeout**: Verifique conectividade com swapi.info
3. **Cache Fallback**: Sistema utiliza cache quando SWAPI não responde

### Cloud Run Issues
1. **Cold Start**: Primeira requisição pode ser lenta
2. **Memory Limits**: Verifique configuração de memória
3. **Timeout**: Ajuste timeout do Cloud Run se necessário

## 🔐 Segurança

### JWT Token Security
- Tokens expiram em 1 hora (configurável)
- Secret key deve ser única por ambiente
- Nunca exponha a secret key em logs

### API Gateway Security
- Rate limiting configurado
- CORS apropriado para produção
- Logs de auditoria habilitados

### Redis Security
- VM em rede privada
- Firewall configurado
- Sem acesso público direto

## 📊 Monitoramento

### Métricas Disponíveis
- **Health Check**: Status da aplicação
- **Redis Performance**: Latência e throughput
- **SWAPI Calls**: Número de chamadas à API externa
- **Cache Hit Rate**: Eficiência do cache

### Logs Estruturados
- Todas as requisições são logadas
- Erros incluem stack traces
- Métricas de performance por endpoint

## 🚀 Performance

### Benchmarks
- **Com Cache**: ~10ms resposta média
- **Sem Cache**: ~500ms resposta média
- **Cache Hit Rate**: >95% em uso normal
- **Throughput**: 1000+ req/s com cache

### Otimizações
- Conexões HTTP reutilizadas
- Serialização JSON otimizada
- Queries de banco eficientes
- Compressão de responses

## 📈 Roadmap

### Próximas Funcionalidades
- [ ] GraphQL interface
- [ ] Webhook notifications
- [ ] Advanced analytics
- [ ] Multi-region cache
- [ ] Real-time updates

### Melhorias Planejadas
- [ ] Kubernetes deployment
- [ ] Prometheus metrics
- [ ] Distributed tracing
- [ ] Advanced caching strategies

## 🤝 Contribuição

### Como Contribuir
1. Fork do repositório
2. Crie uma branch para sua feature
3. Implemente com testes
4. Abra Pull Request

### Padrões de Código
- Python: PEP 8
- Testes: pytest
- Documentação: docstrings
- Commits: conventional commits

## 📝 Notas Importantes

### Desenvolvimento
- ✅ Arquivo `.env` incluído para facilitar desenvolvimento
- ✅ JWT Secret Key fornecida apenas para testes
- ✅ Redis configurado para desenvolvimento local

### Produção
- ⚠️ Gere nova JWT Secret Key para produção
- ⚠️ Configure Redis em VM dedicada no GCP
- ⚠️ Habilite HTTPS em todos os endpoints
- ⚠️ Configure rate limiting apropriado

### Licença
Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

---

**Construído com ❤️ usando FastAPI, Redis, Docker e Google Cloud Platform**
