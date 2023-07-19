import os
import requests
from dotenv import load_dotenv


class DistanceCalculator:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        load_dotenv()
        self.api_key = os.getenv("DISTANCE_KEY")
        self.url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={self.api_key}" \
                   f"&start={self.origin[0]},{self.origin[1]}" \
                   f"&end={self.destination[0]},{self.destination[1]}"

    def calculate_distance(self):
        response = requests.get(self.url)
        data = response.json()
        distance = data["features"][0]["properties"]["segments"][0]["distance"]
        return distance/1000

