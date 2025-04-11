import logging
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.repositories import ReservationRepository, TableRepository
from src.schemas.reservations import CreateReservaionSchema

logger = logging.getLogger(__name__)

class ReservationService:
	def __init__(self, repo: ReservationRepository, table_repo: TableRepository):
		self.repo = repo
		self.table_repo = table_repo
		
	async def get_all(self):
		try:
			logger.info('Получение списка броней')
			result = await self.repo.get_all()
			logger.info('Список броней получен')
			return result
		except SQLAlchemyError as e:
			raise HTTPException(status_code=500, detail='Failed to fetch reservations')
		
	async def create(self, reservation: CreateReservaionSchema):
		try:
			logger.debug('Получение стола с id=%s', reservation.table_id)
			table = await self.table_repo.get(reservation.table_id)
			if not table:
				logger.warning('Стол id=%s не найден', reservation.table_id)
				raise HTTPException(status_code=404, detail='Table not found')
			logger.debug('Получение списка броней в данном временном отрезке')
			get_all_reservations = await self.repo.get_in_reservation_range(reservation.table_id, reservation.reservation_time, reservation.duration_minutes)
			if get_all_reservations:
				logger.warning('Стол в это время уже забронирован')
				raise HTTPException(status_code=400, detail='Table is busy')
			logger.info('Бронирование стола')
			create_reservation = await self.repo.create(reservation.model_dump())
			logger.info('Стол успешно забронирован')
			return create_reservation
		except SQLAlchemyError as e:
			logger.error('Ошибка создания брони: %s', e)
			raise HTTPException(status_code=500, detail='Failed to create reservation')
		
	async def delete(self, id: int):
		try:
			logger.debug('Получение брони с id=%s', id)
			reservation = await self.repo.get(id)
			if not reservation:
				logger.warning('Бронь с id=%s не найдена', id)
				raise HTTPException(status_code=404, detail='Reservation not found')
			logger.info('Удаление брони id=%s', id)
			await self.repo.delete(reservation)
			logger.info('Бронь с id=%s успешно удалена', id)
		except SQLAlchemyError as e:
			logger.error('Ошибка удаления брони: %s', e)
			raise HTTPException(status_code=500, detail='Failed to delete reservation')