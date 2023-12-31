import os
from datetime import datetime
from flask import Flask
from src.controllers.apartment_controller import apartment_blueprint
from src.controllers.owner_controller import owner_blueprint
from src.controllers.client_controller import client_blueprint
from src.controllers.auth_controller import auth_blueprint
from src.controllers.hotel_controller import hotel_blueprint
from src.controllers.opinion_controller import opinion_blueprint
from flasgger import Swagger
from src.controllers.reservation_controller import reservation_blueprint
from src.services.check_reservation_service import reservation_service
from src.services.rabbitmq_service import RabbitMQ
from src.services.seed_service import SeedService
from src.extensions import db


rabbitmq_config = {
    'host': 'localhost',
    'port': 5672,
    'user': 'guest',
    'password': 'guest',
    'queue_name': 'mail_queue',
}


def check_reservations(app):
    with app.app_context():
        reservation_service()
        # print('Reservations checked: %s' % datetime.now())


def create_app():
    app = Flask(__name__)
    app_key = os.getenv("APP_KEY")
    app.config['SECRET_KEY'] = app_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    seed = SeedService()

    rabbitmq = RabbitMQ(rabbitmq_config)

    app.config['RABBITMQ'] = rabbitmq

    with app.app_context():
        db.create_all()
        seed.run()

    app.register_blueprint(owner_blueprint)
    app.register_blueprint(client_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(hotel_blueprint)
    app.register_blueprint(apartment_blueprint)
    app.register_blueprint(opinion_blueprint)
    app.register_blueprint(reservation_blueprint)

    template = {
        "securityDefinitions": {
            "Bearer":
                {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header"
                }
        }
    }

    Swagger(app, template=template)

    return app
