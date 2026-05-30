"""Application configuration.

A lightweight settings object. For richer env/.env handling, swap ``Settings``
for a ``pydantic_settings.BaseSettings`` subclass without touching call sites.
"""

from __future__ import annotations

import os
from functools import lru_cache

from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    """Runtime configuration, resolved once and cached."""

    model_config = ConfigDict(frozen=True)

    project_name: str = "Product Inventory API"
    version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings, overridable via environment."""
    return Settings(
        project_name=os.getenv("PROJECT_NAME", "Product Inventory API"),
        debug=os.getenv("DEBUG", "false").lower() == "true",
    )
