from src.repositories import TableRepository

class TableService:
	def __init__(self, repo: TableRepository):
		self.repo = repo

	async def get_all(self):
		return await self.repo.get_all()