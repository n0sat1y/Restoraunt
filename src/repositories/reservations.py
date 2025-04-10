from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ReservationModel


class ReservationRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get_all(self):
		try:
			query = select(ReservationModel)
			result = await self.session.execute(query)
			reservations = result.scalars().all()
			return reservations
		except Exception as e:
			raise HTTPException(status_code=500, detail=str(e))