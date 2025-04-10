from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TableModel


class TableRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get_all(self):
		try:
			query = select(TableModel)
			result = await self.session.execute(query)
			tables = result.scalars().all()
			return tables
		except Exception as e:
			raise HTTPException(status_code=500, detail=str(e))