from fastapi import APIRouter, Depends

from src.dependencies import get_reservation_service

router = APIRouter(prefix='/reservations', tags=['Reservations'])

@router.get('/')
async def get_all_reservations(_service=Depends(get_reservation_service)):
	return await _service.get_all()

@router.post('/')
async def create_reservations(table: dict):
	return {"message": "reservations created", "table": table}

@router.delete('/{id}')
async def delete_reservations(id: int):
	return {"message": "reservations deleted", "id": id}