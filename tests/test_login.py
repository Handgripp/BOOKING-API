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


def test_should_return_200_on_login(client):
    data = {
        'email': 'johny@doe.com',
        'password': 'qwerty',
    }

    response = client.post('/login', json=data)
    response_json = json.loads(response.data)
    assert response_json["token"] is not None
    assert response.status_code == 200


def test_should_return_401_when_password_is_invalid(client):
    data = {
        'email': 'johny@doe.com',
        'password': 'qqwerty',
    }

    response = client.post('/login', json=data)
    response_json = json.loads(response.data)
    assert response_json["error"] == "Invalid credentials"
    assert response.status_code == 401


def test_should_return_401_when_email_not_confirmed(client):
    data = {
        'email': 'johnyy@doe.com',
        'password': 'qwerty',
    }

    response = client.post('/login', json=data)
    response_json = json.loads(response.data)
    assert response_json["error"] == "Email not confirmed"
    assert response.status_code == 401

