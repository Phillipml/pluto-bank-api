# Pluto Bank API

API REST construída com **FastAPI** para operações bancárias básicas:
- cadastro e listagem de usuários;
- autenticação com JWT;
- consulta de perfil autenticado;
- registro de transações de crédito e débito com atualização de saldo.

A persistência é feita em **SQLite** com **SQLAlchemy** + **databases** (acesso assíncrono), e senhas são armazenadas com hash **Argon2** via `pwdlib`.

## Requisitos

- Python **3.13+**
- [Poetry](https://python-poetry.org/)

## Configuração

Crie um arquivo `.env` na raiz. A variável `JWT_SECRET_KEY` é obrigatória.

| Variável | Obrigatória | Padrão | Descrição |
|----------|-------------|--------|-----------|
| `JWT_SECRET_KEY` | Sim | - | Chave secreta usada para assinar o JWT |
| `JWT_ALGORITHM` | Não | `HS256` | Algoritmo de assinatura do JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Não | `60` | Tempo de expiração do access token (minutos) |
| `DATABASE_URL` | Não | `sqlite:///./bank.db` | URL de conexão com o banco |

Exemplo de `.env`:

```env
JWT_SECRET_KEY=sua_chave_secreta_longa_e_aleatoria
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./bank.db
```

Gerar chave aleatória:

```bash
make get_secret_key
```

## Instalação

```bash
poetry install
```

## Execução

Inicie o servidor em modo de desenvolvimento:

```bash
make server
```

Comando equivalente:

```bash
poetry run uvicorn app.main:app --reload
```

Aplicação:
- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## Endpoints

| Método | Rota | Autenticação | Descrição |
|--------|------|--------------|-----------|
| `GET` | `/health/` | Não | Health check da API |
| `GET` | `/users/` | Não | Lista usuários |
| `POST` | `/users/create` | Não | Cria novo usuário |
| `POST` | `/users/login` | Não | Login e geração de access token |
| `GET` | `/users/me` | Bearer JWT | Retorna usuário autenticado |
| `POST` | `/transactions/` | Bearer JWT | Registra crédito/débito e atualiza saldo |

### Regras relevantes

- O login usa `application/x-www-form-urlencoded` (`username` = e-mail).
- Rotas protegidas exigem `Authorization: Bearer <token>`.
- Na transação, valores positivos representam crédito e negativos representam débito.
- Débitos que deixariam o saldo negativo são rejeitados com `400 Bad Request` e mensagem `Saldo insuficiente`.

## Exemplos rápidos

### 1) Criar usuário

```bash
curl -X POST "http://127.0.0.1:8000/users/create" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Maria Silva\",\"email\":\"maria@email.com\",\"password\":\"12345678\"}"
```

### 2) Login (obter token)

```bash
curl -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=maria@email.com&password=12345678"
```

### 3) Criar transação autenticada

```bash
curl -X POST "http://127.0.0.1:8000/transactions/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d "{\"value\":-50.00,\"description\":\"Compra no mercado\"}"
```

## Desenvolvimento

Formatar código:

```bash
make format
```

## Estrutura do projeto

```text
app/
  main.py              # Inicialização FastAPI e ciclo de vida da conexão
  controllers/         # Rotas HTTP (health, users, transactions)
  core/                # Segurança, settings e dependências
  db/                  # Configuração de engine, database e metadata
  models/              # Definições de tabelas SQLAlchemy
  schemas/             # Schemas Pydantic de request/response
```

## Licença

Consulte o arquivo `LICENSE` na raiz do projeto.
