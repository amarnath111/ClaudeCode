"""Pydantic v2 validation schemas for products.

The schemas separate the three concerns of an API resource:

* ``ProductCreate`` — what a client may send to create a product.
* ``ProductUpdate`` — a partial patch; every field is optional.
* ``ProductRead``   — what the API returns (server-owned fields included).
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Fields common to client-supplied product payloads."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1, max_length=200, description="Human-readable product name.")
    sku: str = Field(min_length=1, max_length=64, description="Stock-keeping unit; unique per product.")
    description: str | None = Field(default=None, max_length=2_000)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2, description="Unit price.")
    quantity: int = Field(ge=0, description="Units currently in stock.")


class ProductCreate(ProductBase):
    """Payload accepted when creating a new product."""


class ProductUpdate(BaseModel):
    """Partial update payload; only the supplied fields are changed."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=200)
    sku: str | None = Field(default=None, min_length=1, max_length=64)
    description: str | None = Field(default=None, max_length=2_000)
    price: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    quantity: int | None = Field(default=None, ge=0)


class ProductRead(ProductBase):
    """Product representation returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
