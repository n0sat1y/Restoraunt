from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.repositories import ReservationRepository, TableRepository
from src.schemas.reservations import CreateReservaionSchema

class ReservationService:
	def __init__(self, repo: ReservationRepository):
		self.repo = repo
		
	async def get_all(self):
		try:
			return await self.repo.get_all()
		except SQLAlchemyError as e:
			raise HTTPException(status_code=500, detail='Failed to fetch reservations')
		
	async def create(self, reservation: CreateReservaionSchema):
		get_all_reservations = await self.repo.get_in_reservation_range(reservation.table_id, reservation.reservation_time, reservation.duration_minutes)
		if get_all_reservations:
			raise HTTPException(status_code=400, detail='Table is busy')
		create_reservation = await self.repo.create(reservation.model_dump())
		return create_reservation