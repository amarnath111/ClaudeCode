"""HTTP routes for the product inventory resource.

The endpoint layer is thin: it validates input via Pydantic schemas, delegates
all rules to :class:`~app.services.product_service.ProductService`, and maps
domain exceptions onto HTTP status codes.
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import (
    DuplicateSKUError,
    ProductNotFoundError,
    ProductService,
    get_product_service,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead], summary="List all products")
def list_products(
    service: ProductService = Depends(get_product_service),
) -> list[ProductRead]:
    return service.list_products()


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product",
)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    try:
        return service.create_product(payload)
    except DuplicateSKUError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/{product_id}", response_model=ProductRead, summary="Get a product")
def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    try:
        return service.get_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{product_id}", response_model=ProductRead, summary="Update a product")
def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    try:
        return service.update_product(product_id, payload)
    except ProductNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DuplicateSKUError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
)
def delete_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
) -> None:
    try:
        service.delete_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
