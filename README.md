# Pluto Bank API

API REST em **FastAPI** para operações bancárias de usuários: cadastro, listagem, autenticação com JWT e perfil autenticado. Persistência em **SQLite** via **SQLAlchemy** + **databases** (acesso assíncrono). Senhas com **Argon2** (`pwdlib`).

## Requisitos

- Python **3.13+**
- [Poetry](https://python-poetry.org/) (gerenciamento de dependências e ambiente virtual)

## Configuração

Crie um arquivo `.env` na raiz do repositório. O `JWT_SECRET_KEY` é **obrigatório** (não há valor padrão em produção).

| Variável | Obrigatória | Padrão | Descrição |
|----------|-------------|--------|-----------|
| `JWT_SECRET_KEY` | Sim | — | Chave secreta para assinar tokens JWT |
| `JWT_ALGORITHM` | Não | `HS256` | Algoritmo do JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Não | `60` | Validade do access token em minutos |
| `DATABASE_URL` | Não | `sqlite:///./bank.db` | URL do banco (SQLite por padrão) |

Exemplo mínimo de `.env`:

```env
JWT_SECRET_KEY=sua_chave_secreta_longa_e_aleatoria
```

Para gerar uma chave aleatória (hex 32 bytes), na raiz do projeto:

```bash
make get_secret_key
```

## Instalação

```bash
poetry install
```

## Executando

Servidor de desenvolvimento com reload:

```bash
make server
```

Equivalente:

```bash
poetry run uvicorn app.main:app --reload
```

Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI).

## Endpoints principais

| Método | Caminho | Autenticação | Descrição |
|--------|---------|--------------|-----------|
| `GET` | `/health/` | Não | Status do servidor |
| `GET` | `/users/` | Não | Lista usuários |
| `POST` | `/users/create` | Não | Cria usuário (corpo JSON) |
| `POST` | `/users/login` | Não | Login (form OAuth2: `username` = e-mail, `password`) |
| `GET` | `/users/me` | Bearer JWT | Dados do usuário logado |

- **Login**: envie `application/x-www-form-urlencoded` com `username` (e-mail) e `password`, conforme `OAuth2PasswordRequestForm`.
- **Rotas protegidas**: header `Authorization: Bearer <access_token>`.

Na criação de usuário, o corpo segue o schema `UserCreate` (nome, e-mail, senha com regras de validação definidas em `app/schemas/users.py`).

## Desenvolvimento

Formatação com Ruff:

```bash
make format
```

## Estrutura do projeto

```
app/
  main.py              # App FastAPI, lifespan (conexão DB, criação de tabelas)
  controllers/         # Rotas (health, users)
  core/                # Configurações, segurança, dependências (JWT)
  db/                  # Database engine e metadata
  models/              # Tabelas SQLAlchemy
  schemas/             # Modelos Pydantic (entrada/saída)
```

## Licença

Veja o arquivo `LICENSE` na raiz do repositório.
