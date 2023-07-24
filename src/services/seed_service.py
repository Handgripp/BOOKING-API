from src.models.client_model import Client
from src.repositories.client_repository import ClientRepository
from src.repositories.owner_repository import OwnerRepository
from src.models.owner_model import Owner


class SeedService:

    def run(self):
        if self.is_database_empty():
            print("Run seeding service")
            self.create_owner()
            self.create_owner_test()
            self.create_owner_without_confirmed_email()
            self.create_client()
            self.create_client_without_confirmed_email()
            print("Seeding completed")

    def create_owner(self):
        owner = OwnerRepository.create_owner("john@doe.com", "qwerty")
        OwnerRepository.email_confirmation(owner["id"])
        return owner["id"]

    def create_owner_test(self):
        owner = OwnerRepository.create_owner_test("3ba523c8-99f8-4779-b4db-416513b2bf85", "test@test.com", "qwerty")
        OwnerRepository.email_confirmation(owner["id"])
        return owner["id"]

    def create_owner_without_confirmed_email(self):
        owner = OwnerRepository.create_owner("johnn@doe.com", "qwerty")
        return owner["id"]

    def create_client(self):
        client = ClientRepository.create_client("Kamil", "Malkowski", "Zieleniewo", "johny@doe.com", "qwerty")
        ClientRepository.email_confirmation(client["id"])
        return client["id"]

    def create_client_without_confirmed_email(self):
        client = ClientRepository.create_client("Kamil", "Malkowski", "Kołobrzeg", "johnyy@doe.com", "qwerty")
        return client["id"]

    def is_database_empty(self):
        owner = Owner.query.limit(1).all()
        client = Client.query.limit(1).all()
        if owner and client:
            return False

        return True
