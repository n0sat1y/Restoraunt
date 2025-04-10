from fastapi import APIRouter

router = APIRouter(prefix='/reservations', tags=['Reservations'])

@router.get('/')
async def get_reservations():
	return {"message": "List of reservations"}

@router.post('/')
async def create_reservations(table: dict):
	return {"message": "reservations created", "table": table}

@router.delete('/{id}')
async def delete_reservations(id: int):
	return {"message": "reservations deleted", "id": id}