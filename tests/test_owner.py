import pytest
from src.app import create_app
from src.extensions import db
from src.services.seed_service import SeedService


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    seed = SeedService()

    with app.app_context():
        db.drop_all()
        db.create_all()
        seed.run()

    with app.test_client() as client:
        yield client


def test_should_return_201_on_create_owner(client):
    data = {
        'email': 'johndaaoe@example.com',
        'password': 'secretpassword'
    }

    response = client.post('/owners', json=data)

    assert response.status_code == 201


def test_should_return_400_on_create_owner(client):
    data = {
        'email': 'johndaao.com',
        'password': 'secretpassword'
    }

    response = client.post('/owners', json=data)

    assert response.status_code == 400
