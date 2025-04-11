import logging
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from src.repositories import TableRepository
from src.schemas.tables import CreateTableSchema

logger = logging.getLogger(__name__)

class TableService:
	def __init__(self, repo: TableRepository):
		self.repo = repo

	async def get_all(self):
		try:
			logger.info('Получение списка столов')
			tables = await self.repo.get_all()
			logger.info('Список столов получен')
			return tables
		except SQLAlchemyError as e:
			logger.error('Ошибка получения списка столов: %s', e)
			raise HTTPException(status_code=500, detail='Failed to fetch tables')

	async def create(self, table: CreateTableSchema):
		logger.debug('Получение стола по имени: %s', table.name)
		get_table = await self.repo.get_by_name(table.name)
		if get_table:
			logger.warning('Стол с именем %s уже существует', table.name)
			raise HTTPException(status_code=400, detail='A table with that name has already been created')
		try:
			logger.info('Создание стола: %s', table.name)
			create_table = await self.repo.create(table.model_dump())
			logger.info('Стол %s создан', create_table.name)
			return create_table
		except SQLAlchemyError as e:
			logger.error('Ошибка создания стола: %s', e)
			raise HTTPException(status_code=500, detail='Failed to create table')
	
	async def delete(self, id: int):
		logger.debug('Получение стола по id: %s', id)
		table = await self.repo.get(id)
		if not table:
			logger.warning('Стол с id=%s не найден', id)
			raise HTTPException(status_code=404, detail='Table not found')
		try:
			logger.info('Удаление стола с id=%s', id)
			await self.repo.delete(table)
			logger.info('Стол id=%s успешно удален', id)
		except SQLAlchemyError as e:
			logger.error('Ошибка удаления стола: %s', e)
			raise HTTPException(status_code=500, detail='Failed to delete table')
			