import pytest
from datetime import datetime, timezone

from tests.test_tables import table_repo, table_dict
from src.repositories import ReservationRepository
from src.services import ReservationService
from src.schemas.reservations import CreateReservaionSchema

@pytest.fixture
async def table(table_repo, table_dict):
	return await table_repo.create(table_dict)

@pytest.fixture
def res_dict(table):
	return {
		'customer_name': 'some name',
		'reservation_time': datetime.now(timezone.utc),
		'duration_minutes': 60,
		'table_id': table.id
	}

@pytest.fixture
def res_schema(res_dict):
	return CreateReservaionSchema(**res_dict)


@pytest.fixture
def res_repo(session):
	return ReservationRepository(session)

@pytest.fixture
def res_service(table_repo, res_repo):
	return ReservationService(res_repo, table_repo)

async def test_get_repo(res_repo):
	result = await res_repo.get(1)
	assert result is None

async def test_get_all_repo(res_repo):
	result = await res_repo.get_all()
	assert result == []

async def test_get_in_reservation_range_repo(res_repo, table, res_dict):
	result = await res_repo.get_in_reservation_range(
		table_id=table.id,
		reservation_time=res_dict['reservation_time'],
		duration_minutes=res_dict['duration_minutes']
	)
	assert result == []

async def test_create_repository(res_repo, res_dict):
	result = await res_repo.create(res_dict)
	assert result.id

async def test_delete_repository(res_repo, res_dict):
	res = await res_repo.create(res_dict)
	result = await res_repo.delete(res)
	assert not result

async def test_get_all_service(res_service):
	result = await res_service.get_all()
	assert result == []

async def test_create_service(res_service, res_schema):
	result = await res_service.create(res_schema)
	assert result.id

async def test_delete_service(res_service, res_dict, res_repo):
	await res_repo.create(res_dict)
	result = await res_service.delete(1)
	assert not result

async def test_get_all(client):
	response = await client.get('/api/v1/reservations/')
	assert response.status_code == 200
	assert response.json() == []

async def test_create(client, res_dict):
	res_dict['reservation_time'] = str(res_dict['reservation_time'])
	response = await client.post('/api/v1/reservations/', json=res_dict)
	assert response.status_code == 200
	data = response.json()
	assert data['id'] is not None

async def test_delete(client, res_schema, res_service):
	res = await res_service.create(res_schema)
	response = await client.delete('/api/v1/reservations/1')
	assert response.status_code == 200
	assert response.json() == {'message': 'Reservation deleted successfully'}