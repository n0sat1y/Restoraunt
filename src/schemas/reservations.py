from datetime import datetime
from pydantic import BaseModel

class CreateReservaionSchema(BaseModel):
	customer_name: str
	reservation_time: datetime
	duration_minutes: int
	table_id: int