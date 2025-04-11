import pytest

from src.repositories import TableRepository
from src.services import TableService
from src.schemas.tables import CreateTableSchema

@pytest.fixture
def table_dict():
	return {
		'name': 'some name',
		'seats': 10,
		'location': 'some location'	
	}

@pytest.fixture
def table_schema(table_dict):
	return CreateTableSchema(**table_dict)

@pytest.fixture
def table_repo(session):
	return TableRepository(session)

@pytest.fixture
def table_service(table_repo):
	return TableService(table_repo)

async def test_get_repository(table_repo):
	result = await table_repo.get(1)
	assert result is None

async def test_get_by_name_repository(table_repo):
	result = await table_repo.get_by_name('some str')
	assert result is None

async def test_get_all_repository(table_repo):
	result = await table_repo.get_all()
	assert result == []

async def test_create_repository(table_repo, table_dict):
	result = await table_repo.create(table_dict)
	assert result.id == 1

async def test_delete_repository(table_repo, table_dict):
	print(await table_repo.get_all())
	table = await table_repo.create(table_dict)
	result = await table_repo.delete(table)
	assert result is None

async def test_get_all_service(table_service):
	result = await table_service.get_all()
	assert result == []

async def test_create_service(table_service, table_schema):
	result = await table_service.create(table_schema)
	assert result.id

async def test_delete_service(table_service, table_schema):
	table = await table_service.create(table_schema)
	result = await table_service.delete(table.id)
	assert result is None

async def test_get_all(client):
	response = await client.get('/api/v1/tables/')
	assert response.status_code == 200
	assert response.json() == []

async def test_create(client, table_dict):
	response = await client.post('/api/v1/tables/', json=table_dict)
	assert response.status_code == 200
	data = response.json()
	assert data['id'] is not None

async def test_delete(client, table_schema, table_service):
	table = await table_service.create(table_schema)
	response = await client.delete('/api/v1/tables/1')
	assert response.status_code == 200
	assert response.json() == {'message': 'Table deleted successfully'}
