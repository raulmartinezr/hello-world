# Hello World

CLI generado desde plantilla (uv + Typer + pytest-bdd + devcontainer).

## Requisitos
- Python 3.13+
- uv (https://docs.astral.sh/uv/)

## Setup
```bash
uv sync --all-extras --dev
```

## Ejecutar
```bash
uv run hello-world --version
uv run hello-world hello say Alice
```

## Tests
```bash
uv run pytest
uv run pytest -m bdd
uv run pytest --cov
```

## Calidad
```bash
uv run ruff check .
uv run ruff format .
uv run mypy src
uv run pre-commit run -a
    ```
    

# Copier Template: Python + uv + Typer + pytest-bdd + Devcontainer

Plantilla para crear CLIs en Python gestionados con **uv**, **Typer** y **pytest-bdd**, con
**devcontainers**, **ruff**, **mypy** y **pre-commit**.

## Uso rápido

```bash
# Crear proyecto desde esta plantilla (local o remoto)
uvx copier copy --trust /path/to/python-uv-typer-template .
# o: uvx copier copy --trust gh:your-org/python-uv-typer-template .

cd hello-world/
uv sync --all-extras --dev
uv run hello_world --version
uv run pytest
    ```


# Python module structure


hello-world/
├─ pyproject.toml
├─ README.md
├─ .env.example
├─ alembic.ini
├─ migrations/                 # Alembic revision scripts
│  └─ versions/
├─ src/
│  └─ hello_world/
│     ├─ app/
│     │  ├─ main.py            # FastAPI factory + router wiring
│     │  ├─ api/
│     │  │  ├─ deps.py         # FastAPI deps (DB session, auth, etc.)
│     │  │  ├─ router.py       # Root API router
│     │  │  ├─ v1/
│     │  │  │  ├─ users.py     # HTTP endpoints for users domain
│     │  │  │  └─ orders.py    # (example second domain)
│     │  └─ lifecycles.py      # startup/shutdown events
│     │
│     ├─ cli/
│     │  ├─ __main__.py        # `python -m myapp.cli`
│     │  ├─ cli.py             # Typer app factory
│     │  ├─ users.py           # CLI for users domain
│     │  └─ orders.py          # CLI for orders domain
│     │
│     ├─ core/
│     │  ├─ config.py          # Settings (Pydantic), env handling
│     │  ├─ db.py              # Engine/session management
│     │  ├─ security.py        # (optional) password hashing/JWT tools
│     │  └─ logging.py         # structured logging config
│     │
│     ├─ domains/
│     │  ├─ users/
│     │  │  ├─ models.py       # SQLAlchemy models
│     │  │  ├─ schemas.py      # Pydantic DTOs
│     │  │  ├─ repository.py   # Data access
│     │  │  ├─ service.py      # Business logic/use cases
│     │  │  └─ __init__.py
│     │  └─ orders/
│     │     ├─ models.py
│     │     ├─ schemas.py
│     │     ├─ repository.py
│     │     ├─ service.py
│     │     └─ __init__.py
│     │
│     └─ utils/
│        └─ pagination.py      # shared helpers
│
└─ tests/
   ├─ conftest.py
   ├─ integration/
   │  └─ test_users_api.py
   └─ unit/
      ├─ test_users_service.py
      └─ test_users_repo.py

domains
['users', 'orders']

domains_csv
users,orders

Parsed
users.py.jinjaorders.py.jinja