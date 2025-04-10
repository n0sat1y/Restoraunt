from fastapi import APIRouter, Depends

from src.dependencies import get_table_service

router = APIRouter(prefix='/tables', tags=['Tables'])

@router.get('/')
async def get_all_tables(_service=Depends(get_table_service)):
	return await _service.get_all()

@router.post('/')
async def create_table(table: dict):
	return {"message": "Table created", "table": table}

@router.delete('/{id}')
async def delete_table(id: int):
	return {"message": "Table deleted", "id": id}