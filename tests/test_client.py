import json

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


def test_should_return_201_on_create_client(client):
    data = {
        'first_name': 'Kamil',
        'last_name': 'Malkowski',
        'email': 'johndaaoe@example.com',
        'password': 'secretpassword',
        'city': 'Kolobrzeg'
    }

    response = client.post('/clients', json=data)

    assert response.status_code == 201


def test_should_return_400_on_create_client(client):
    data = {
        'first_name': 'Kamil',
        'last_name': 'Malkowski',
        'city': 'Kolobrzeg',
        'email': 'johndaao.com',
        'password': 'secretpassword'
    }

    response = client.post('/clients', json=data)

    assert response.status_code == 400


def test_should_return_404_on_wrong_city(client):
    data = {
        'first_name': 'Kamil',
        'last_name': 'Malkowski',
        'city': 'Aaaaavvv',
        'email': 'johny@dooe.com',
        'password': 'secretpassword'
    }

    response = client.post('/clients', json=data)
    response_json = json.loads(response.data)
    assert response_json["error"] == "City does not exist"
    assert response.status_code == 404


def test_should_return_409_on_create_client(client):
    data = {
        'first_name': 'Kamil',
        'last_name': 'Malkowski',
        'city': 'Kolobrzeg',
        'email': 'johny@doe.com',
        'password': 'secretpassword'
    }

    response = client.post('/clients', json=data)

    assert response.status_code == 409
