from src.models.client_model import Client
from src.repositories.client_repository import ClientRepository
from src.repositories.owner_repository import OwnerRepository
from src.models.owner_model import Owner


class SeedService:

    def run(self):
        if self.is_database_empty():
            print("Run seeding service")
            self.create_owner()
            self.create_client()
            print("Seeding completed")

    def create_owner(self):
        owner = OwnerRepository.create_owner("john@doe.com", "qwerty")
        OwnerRepository.email_confirmation(owner["id"])
        return owner["id"]

    def create_client(self):
        client = ClientRepository.create_client("Kamil", "Malkowski", "Kolobrzeg", "johny@doe.com", "qwerty")
        ClientRepository.email_confirmation(client["id"])
        return client["id"]

    def is_database_empty(self):
        owner = Owner.query.limit(1).all()
        client = Client.query.limit(1).all()
        if owner and client:
            return False

        return True
