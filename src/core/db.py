from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core.config import settings

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

