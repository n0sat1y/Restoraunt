from src.repositories import ReservationRepository

class ReservationService:
	def __init__(self, repo: ReservationRepository):
		self.repo = repo
		
	async def get_all(self):
		return await self.repo.get_all()