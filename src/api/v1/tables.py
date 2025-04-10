from fastapi import APIRouter

router = APIRouter(prefix='/tables', tags=['Tables'])

@router.get('/')
async def get_tables():
	return {"message": "List of tables"}

@router.post('/')
async def create_table(table: dict):
	return {"message": "Table created", "table": table}

@router.delete('/{id}')
async def delete_table(id: int):
	return {"message": "Table deleted", "id": id}