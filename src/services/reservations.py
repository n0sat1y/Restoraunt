from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.repositories import ReservationRepository, TableRepository
from src.schemas.reservations import CreateReservaionSchema

class ReservationService:
	def __init__(self, repo: ReservationRepository, table_repo: TableRepository):
		self.repo = repo
		self.table_repo = table_repo
		
	async def get_all(self):
		try:
			return await self.repo.get_all()
		except SQLAlchemyError as e:
			raise HTTPException(status_code=500, detail='Failed to fetch reservations')
		
	async def create(self, reservation: CreateReservaionSchema):
		try:
			table = await self.table_repo.get(reservation.table_id)
			if not table:
				raise HTTPException(status_code=404, detail='Table not found')
			get_all_reservations = await self.repo.get_in_reservation_range(reservation.table_id, reservation.reservation_time, reservation.duration_minutes)
			if get_all_reservations:
				raise HTTPException(status_code=400, detail='Table is busy')
			create_reservation = await self.repo.create(reservation.model_dump())
			return create_reservation
		except SQLAlchemyError as e:
			raise HTTPException(status_code=500, detail='Failed to create reservation')