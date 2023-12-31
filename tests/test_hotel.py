import pytest
from src.app import create_app
from src.extensions import db
from src.services.seed_service import SeedService
from flask_jwt_extended import JWTManager

from tests.jwt import access_token_owner


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_TOKEN_LOCATION'] = 'json'
    JWTManager(app)

    seed = SeedService()

    with app.app_context():
        db.drop_all()
        db.create_all()
        seed.run()

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_should_return_201_on_create_hotel(client):

    headers = {'Authorization': f'Bearer {access_token_owner}'}

    data = {
        'city': 'Kołobrzeg',
        'hotel_name': 'Diune',
    }

    response = client.post('/hotels', json=data, headers=headers)

    assert response.status_code == 201

