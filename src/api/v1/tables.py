from fastapi import APIRouter, Depends

from src.dependencies import get_table_service
from src.schemas.tables import CreateTableSchema, GetTableSchema

router = APIRouter(prefix='/tables', tags=['Tables'])

@router.get('/')
async def get_all_tables(_service=Depends(get_table_service)) -> list[GetTableSchema]:
	return await _service.get_all()

@router.post('/')
async def create_table(
	table: CreateTableSchema,
	_service=Depends(get_table_service)
) -> GetTableSchema:
	return await _service.create(table)

@router.delete('/{id}')
async def delete_table(id: int, _service=Depends(get_table_service)):
	await _service.delete(id)
	return {'message': 'Table deleted successfully'}