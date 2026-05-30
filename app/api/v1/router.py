"""Aggregates all v1 endpoint routers under a single API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import products

api_router = APIRouter()
api_router.include_router(products.router)
