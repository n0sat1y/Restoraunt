from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}

class Base(DeclarativeBase):
	metadata = MetaData(naming_convention=convention)

class DataBase:
	def __init__(self):
		self.engine = create_async_engine(
			url=settings.DB_URL
		)
		self.sessionlocal = async_sessionmaker(
			bind=self.engine,
			expire_on_commit=False
		)

	async def session(self):
		async with self.sessionlocal() as session:
			yield session

	async def close(self):
		await self.engine.dispose()

db = DataBase()

