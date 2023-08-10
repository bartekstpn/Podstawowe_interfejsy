import json

import requests
from geopy import Nominatim
from datetime import datetime, timedelta


API_URL = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" \
          "&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"

class WeatherForecast:

    def __init__(self):
        try:
            self.city = input("Podaj miasto, dla którego chcesz sprawdzić pogodę: ")
            self.date = input("Podaj datę, dla której chcesz sprawdzić pogodę: (YYYY-MM-DD)")
            if not self.date:
                self.date = datetime.now()
                self.date = self.date + timedelta(1)
                self.date = self.date.strftime('%Y-%m-%d')
                print("Nie podano daty, wyświetlono najbliższy dzień")
        except:
            print("Nie znaleziono miasta lub podano datę w złym formacie")
        self.weather_forecast = self.load_data_from_file()

    def load_data_from_file(self):
        with open("opady.txt", mode="a+") as file:
            data_in_file = file.read()

        return json.loads(data_in_file) if data_in_file else {}


    def retrieve_data_from_api(self, latitude, longitude):
        response = requests.get(API_URL.format(latitude=latitude, longitude=longitude, searched_date=self.date))
        data = json.loads(response.text)
        return data

    def find_coordinates_for_city(self):
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(self.city)
        return location.latitude, location.longitude

    def check_raining_sum(self, data):
        raining_sum = data.get("daily").get("rain_sum")[0]
        if raining_sum > 0.0:
            return "Bedzie padać"
        elif raining_sum == 0.0:
            return "Nie bedzie padac"
        else:
            return "Nie wiem"

    def retrieve_data(self):
        city_data = self.weather_forecast.get(self.city)
        if city_data:
            if city_data.get(self.date):
                return city_data[self.date], False
        latitude, longitude = self.find_coordinates_for_city()
        data = self.retrieve_data_from_api(latitude, longitude)
        raining_data = self.check_raining_sum(data)
        return raining_data, True

    def transform_data_in_file(self, raining_info):
        if self.weather_forecast.get(self.city):
            self.weather_forecast[self.city][self.date] = raining_info
        else:
            self.weather_forecast[self.city] = {}
            self.weather_forecast[self.city][self.date] = raining_info
        return json.dumps(self.weather_forecast).replace("'", '"')

    def write_data_to_file(self, raining_info):
        with open("opady.txt", mode="a+") as file:
            new_data = self.transform_data_in_file(raining_info)
            file.write(new_data)
            print(new_data)

    def items(self):
        for city in self.weather_forecast.keys():
            for date in self.weather_forecast.get(city).keys():
                yield date, city

    def __iter__(self):
        return iter(self.weather_forecast)

    def __setitem__(self, key, value):
        city, data = key
        self.weather_forecast[city][data] = value

    def __getitem__(self, item):
        city, data = item
        return self.weather_forecast[city][data]