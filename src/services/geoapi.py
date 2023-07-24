import os
import requests
from dotenv import load_dotenv


class CityChecker:
    def __init__(self, city):
        self.city = city
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.url = f"https://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=1&appid={self.api_key}"
        self.exists = False
        self.coordinates = None

    def check_city_existence(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            if data:
                self.exists = True
                return self.exists

    def get_city_coordinates(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            self.coordinates = {
                "lat": data[0]["lat"],
                "lon": data[0]["lon"]
            }
            return self.coordinates
