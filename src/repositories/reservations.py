from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import ReservationModel


class ReservationRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get(self, id: int):
		try:
			query = select(ReservationModel).where(ReservationModel.id == id)
			result = await self.session.execute(query)
			tables = result.scalar_one_or_none()
			return tables
		except SQLAlchemyError as e:
			raise 

	async def get_all(self):
		try:
			query = select(ReservationModel)
			result = await self.session.execute(query)
			reservations = result.scalars().all()
			return reservations
		except SQLAlchemyError as e:
			raise 

	async def get_in_reservation_range(self, 
		table_id: int, 
		reservation_time: datetime, 
		duration_minutes: int
	):
		try:
			query = (
				select(ReservationModel).
				where(ReservationModel.table_id == table_id).
				filter(
					ReservationModel.reservation_time + timedelta(minutes=ReservationModel.duration_minutes) >= reservation_time, 
					ReservationModel.reservation_time <= reservation_time + timedelta(minutes=duration_minutes)
				)
			)
			result = await self.session.execute(query)
			tables = result.scalars().all()
			return tables
		except SQLAlchemyError as e:
			raise 

	async def create(self, reservation: dict):
		try:
			new_table = ReservationModel(**reservation)
			self.session.add(new_table)
			await self.session.commit()
			return new_table
		except SQLAlchemyError as e:
			raise 

	async def delete(self, reservation: ReservationModel):
		try:
			await self.session.delete(reservation)
			await self.session.commit()
			return None
		except SQLAlchemyError as e:
			raise 