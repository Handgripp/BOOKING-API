from flask import Flask
from extensions import db
from controllers.owner_controller import owner_blueprint
from flasgger import Swagger
from services.seed_service import SeedService


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    seed = SeedService()

    with app.app_context():
        db.create_all()
        seed.run()

    app.register_blueprint(owner_blueprint)

    Swagger(app)



    return app
