import uuid

from src.models.client_model import Client
from src.models.opinion_model import Opinion, db


class OpinionRepository:

    @staticmethod
    def create_opinion(hotel_id, client_id, text, rating):
        opinion = Opinion(id=str(uuid.uuid4()), hotel_id=hotel_id, client_id=client_id, text=text, rating=rating)
        db.session.add(opinion)
        db.session.commit()
        opinion_data = {
            'id': opinion.id,
            'created_at': opinion.created_at,
            'updated_at': opinion.updated_at,
            'hotel_id': opinion.hotel_id,
            'text': opinion.text,
            'rating': opinion.rating
        }

        return opinion_data

    @staticmethod
    def get_one_by_id(hotel_id, opinion_id):
        opinion = Opinion.query.filter_by(id=opinion_id, hotel_id=hotel_id).first()
        client = Client.query.filter_by(id=opinion.client_id).first()

        if not opinion:
            return None

        opinion_data = {
            'id': opinion.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'created_at': opinion.created_at,
            'updated_at': opinion.updated_at,
            'hotel_id': opinion.hotel_id,
            'client_id': opinion.client_id,
            'text': opinion.text,
            'rating': opinion.rating
        }

        return opinion_data

    @staticmethod
    def get_all(hotel_id):
        opinions = Opinion.query.filter_by(hotel_id=hotel_id).all()

        if not opinions:
            return None

        opinions_data = []
        for opinion in opinions:
            client = Client.query.filter_by(id=opinion.client_id).first()
            opinion_data = {
                'id': opinion.id,
                'first_name': client.first_name,
                'last_name': client.last_name,
                'created_at': opinion.created_at,
                'updated_at': opinion.updated_at,
                'hotel_id': opinion.hotel_id,
                'client_id': opinion.client_id,
                'text': opinion.text,
                'rating': opinion.rating
            }
            opinions_data.append(opinion_data)

        return opinions_data
