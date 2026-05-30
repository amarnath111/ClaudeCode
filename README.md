# Product Inventory API

A production-ready FastAPI REST API for managing a product inventory, built with
Python 3.11+ strict typing, Pydantic v2, and Poetry.

## Setup

```bash
poetry install
```

## Run

```bash
poetry run uvicorn app.main:app --reload
```

- Interactive docs: http://127.0.0.1:8000/docs
- Health probe:     http://127.0.0.1:8000/health

## Test & type-check

```bash
poetry run pytest
poetry run mypy .
```

## Layout

```
app/
  main.py                       # App factory + health route
  core/config.py                # Settings
  api/v1/router.py              # Aggregates v1 routers
  api/v1/endpoints/products.py  # Product HTTP routes
  schemas/product.py            # Pydantic v2 request/response models
  services/product_service.py   # Business logic (storage-agnostic)
tests/
  test_products.py              # End-to-end wiring tests
```

The endpoint layer is thin and delegates all domain rules to the service layer,
which is storage-agnostic (currently in-memory) so the backing store can be
swapped for a database without touching routes.
