from fastapi import APIRouter, Depends

from src.dependencies import get_reservation_service
from src.schemas.reservations import CreateReservaionSchema

router = APIRouter(prefix='/reservations', tags=['Reservations'])

@router.get('/')
async def get_all_reservations(_service=Depends(get_reservation_service)):
	return await _service.get_all()

@router.post('/')
async def create_reservations(
	reservation: CreateReservaionSchema, 
	_service=Depends(get_reservation_service)
):
	return await _service.create(reservation)

@router.delete('/{id}')
async def delete_reservations(id: int, _service=Depends(get_reservation_service)):
	await _service.delete(id)
	return {'message': 'Reservation deleted successfully'}