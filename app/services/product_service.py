"""Business-logic layer for product inventory.

This module owns all domain rules (uniqueness of SKU, existence checks) and is
deliberately storage-agnostic: it currently keeps products in memory, but the
public method signatures form a contract the API layer depends on, so the
backing store can be replaced with a database/repository without changing
endpoints.
"""

from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from threading import Lock
from uuid import UUID, uuid4

from app.schemas.product import ProductCreate, ProductRead, ProductUpdate


class ProductServiceError(Exception):
    """Base class for recoverable product-service errors."""


class ProductNotFoundError(ProductServiceError):
    """Raised when a referenced product does not exist."""

    def __init__(self, product_id: UUID) -> None:
        super().__init__(f"Product {product_id} not found")
        self.product_id = product_id


class DuplicateSKUError(ProductServiceError):
    """Raised when a product SKU collides with an existing one."""

    def __init__(self, sku: str) -> None:
        super().__init__(f"Product with SKU '{sku}' already exists")
        self.sku = sku


class ProductService:
    """In-memory implementation of the product inventory store."""

    def __init__(self) -> None:
        self._items: dict[UUID, ProductRead] = {}
        self._lock = Lock()

    def list_products(self) -> list[ProductRead]:
        """Return all products in insertion order."""
        return list(self._items.values())

    def get_product(self, product_id: UUID) -> ProductRead:
        """Return a single product or raise :class:`ProductNotFoundError`."""
        try:
            return self._items[product_id]
        except KeyError as exc:
            raise ProductNotFoundError(product_id) from exc

    def create_product(self, payload: ProductCreate) -> ProductRead:
        """Create and persist a new product, enforcing SKU uniqueness."""
        with self._lock:
            self._ensure_unique_sku(payload.sku)
            now = datetime.now(timezone.utc)
            product = ProductRead(
                id=uuid4(),
                created_at=now,
                updated_at=now,
                **payload.model_dump(),
            )
            self._items[product.id] = product
            return product

    def update_product(self, product_id: UUID, payload: ProductUpdate) -> ProductRead:
        """Apply a partial update to an existing product."""
        with self._lock:
            current = self.get_product(product_id)
            changes = payload.model_dump(exclude_unset=True)
            new_sku = changes.get("sku")
            if new_sku is not None and new_sku != current.sku:
                self._ensure_unique_sku(new_sku)
            updated = current.model_copy(
                update={**changes, "updated_at": datetime.now(timezone.utc)}
            )
            self._items[product_id] = updated
            return updated

    def delete_product(self, product_id: UUID) -> None:
        """Delete a product or raise :class:`ProductNotFoundError`."""
        with self._lock:
            if product_id not in self._items:
                raise ProductNotFoundError(product_id)
            del self._items[product_id]

    def _ensure_unique_sku(self, sku: str) -> None:
        if any(existing.sku == sku for existing in self._items.values()):
            raise DuplicateSKUError(sku)


@lru_cache
def get_product_service() -> ProductService:
    """Provide a process-wide singleton service for dependency injection.

    Tests can reset state with ``get_product_service.cache_clear()`` or override
    the dependency on the FastAPI app.
    """
    return ProductService()
