from src.repositories.owner_repository import OwnerRepository
from src.models.owner_model import Owner


class SeedService:

    def run(self):
        if self.is_database_empty():
            print("Run seeding service")
            self.create_owner()
            print("Seeding completed")

    def create_owner(self):
        owner = OwnerRepository.create_owner("john@doe.com", "qwerty")
        OwnerRepository.email_confirmation(owner["id"])
        return owner["id"]

    def is_database_empty(self):
        user_data = Owner.query.limit(1).all()
        if user_data:
            return False

        return True
