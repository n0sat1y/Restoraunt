from pydantic import BaseModel

class CreateTableSchema(BaseModel):
	name: str
	seats: int
	location: str

class GetTableSchema(CreateTableSchema):
	id: int
