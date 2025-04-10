from fastapi import APIRouter
from src.api.v1.tables import router as tables_router
from src.api.v1.reservations import router as reservations_router

router = APIRouter(prefix='/v1')
router.include_router(tables_router)
router.include_router(reservations_router)

__all__ = [
	'router'
]