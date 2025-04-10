from fastapi import APIRouter
from src.api.v1 import router


router = APIRouter(prefix='/api')
router.include_router(router)


__all__ = [
	'router'
]