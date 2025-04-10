from src.repositories import TableRepository
from src.schemas.tables import CreateTableSchema

class TableService:
	def __init__(self, repo: TableRepository):
		self.repo = repo

	async def get_all(self):
		return await self.repo.get_all()
	
	async def create(self, table: CreateTableSchema):
		return await self.repo.create(table.model_dump())