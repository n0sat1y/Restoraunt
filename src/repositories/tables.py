from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.models import TableModel


class TableRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get(self, id: int):
		try:
			query = select(TableModel).where(TableModel.id == id)
			result = await self.session.execute(query)
			tables = result.scalar_one_or_none()
			return tables
		except SQLAlchemyError as e:
			raise 

	async def get_by_name(self, name: str):
		try:
			query = select(TableModel).where(TableModel.name == name)
			result = await self.session.execute(query)
			tables = result.scalar_one_or_none()
			return tables
		except SQLAlchemyError as e:
			raise 

	async def get_all(self):
		try:
			query = select(TableModel)
			result = await self.session.execute(query)
			tables = result.scalars().all()
			return tables
		except SQLAlchemyError as e:
			raise 
		
	async def create(self, table: dict):
		try:
			new_table = TableModel(**table)
			self.session.add(new_table)
			await self.session.commit()
			return new_table
		except SQLAlchemyError as e:
			raise 
		
	async def delete(self, Table: TableModel):
		try:
			await self.session.delete(Table)
			await self.session.commit()
			return None
		except SQLAlchemyError as e:
			raise 