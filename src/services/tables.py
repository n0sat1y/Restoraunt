from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.repositories import TableRepository
from src.schemas.tables import CreateTableSchema

class TableService:
	def __init__(self, repo: TableRepository):
		self.repo = repo

	async def get_all(self):
		try:
			return await self.repo.get_all()
		except SQLAlchemyError as e:
			raise HTTPException(status_code=500, detail='Failed to fetch tables')

	async def create(self, table: CreateTableSchema):
		get_table = await self.repo.get_by_name(table.name)
		if get_table:
			raise HTTPException(status_code=400, detail='A table with that name has already been created')
		try:
			return await self.repo.create(table.model_dump())
		except SQLAlchemyError as e:
			raise HTTPException(status_code=500, detail='Failed to create table')
	
	async def delete(self, id: int):
		table = await self.repo.get(id)
		if not table:
			raise HTTPException(status_code=404, detail='Table not found')
		try:
			return await self.repo.delete(table)
		except SQLAlchemyError as e:
			raise HTTPException(status_code=500, detail='Failed to delete table')
			