import pytest
from fastapi.testclient import TestClient
from app.frameworks_and_drivers.api.api import app

@pytest.fixture(scope="function")
def setup_database():
    from app.frameworks_and_drivers.database.sqlite_handler import SQLiteHandler
    from app.interface_adapters.repositories.movie_repository import MovieRepository
    from app.interface_adapters.controllers.producer_controller import ProducerController

    db_handler = SQLiteHandler()
    movie_repository = MovieRepository(db_handler.get_connection())
    producer_controller = ProducerController(movie_repository)
    # Setup your test data here.

def test_get_producer_intervals():
    client = TestClient(app)
    response = client.get("/producers/intervals")
    assert response.status_code == 200