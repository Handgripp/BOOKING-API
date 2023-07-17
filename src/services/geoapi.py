import requests


class CityChecker:
    def __init__(self, city):
        self.city = city
        self.api_key = "8bd61fd34948f6e33e20c26d833e6429"
        self.url = f"https://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=1&appid={self.api_key}"
        self.exists = False

    def check_city_existence(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            if data:
                self.exists = True
                return self.exists

        return False
