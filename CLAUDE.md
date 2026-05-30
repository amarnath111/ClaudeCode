# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech stack & conventions

This project is built with the following stack. Adhere to these choices when adding or
modifying code; do not introduce alternative frameworks or libraries without being asked.

- **Web framework: FastAPI.** Build APIs with FastAPI routers, dependency injection
  (`Depends`), and `async def` endpoints. Use FastAPI's native request/response models
  (Pydantic) rather than hand-rolling serialization.
- **Language: Python 3.11+ with strict type hinting.** Every function signature, parameter,
  and return value must be fully annotated. Prefer modern syntax (`list[str]`, `dict[str, int]`,
  `X | None` instead of `Optional[X]`, `match` statements where they read clearly). Code should
  pass a strict type checker (e.g. `mypy --strict` or Pyright strict) with no `Any` escapes
  unless genuinely unavoidable and commented.
- **Data validation: Pydantic v2.** Define request/response and domain models as
  `pydantic.BaseModel` (or `pydantic.dataclasses`). Use v2 idioms: `model_config = ConfigDict(...)`,
  `@field_validator` / `@model_validator`, `model_dump()` / `model_validate()`. Do **not** use
  deprecated v1 APIs (`.dict()`, `.parse_obj()`, `class Config:`, `@validator`).
- **Dependency isolation: Poetry or Pipenv.** Manage dependencies and the virtualenv through
  one of these tools — never install into the system interpreter. Keep the lockfile
  (`poetry.lock` / `Pipfile.lock`) committed and in sync with the manifest.

## Commands

The exact commands depend on which dependency manager is in use:

```bash
# Poetry
poetry install                 # install deps into the managed venv
poetry run uvicorn app.main:app --reload   # run the FastAPI dev server
poetry run pytest              # run tests
poetry run mypy .              # strict type check

# Pipenv
pipenv install --dev           # install deps
pipenv run uvicorn app.main:app --reload   # run the FastAPI dev server
pipenv run pytest              # run tests
pipenv run mypy .              # strict type check
```

Adjust `app.main:app` to the actual module path of the FastAPI `app` instance once it exists.

## Notes

- The repo currently contains only a PyCharm starter `main.py`; the structure above is the
  target convention as real code lands.
- `.idea/misc.xml` references the **Black** formatter — format with Black to match the IDE.
- This file governs the `ClaudeCode/` repo only. The parent `/Users/amar/CLAUDE.md` documents
  the broader home-directory layout.
