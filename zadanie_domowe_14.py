'''
Napisz program, który sprawdzi, czy danego dnia będzie padać. Użyj do tego poniższego API. Aplikacja ma działać następująco:

Program pyta dla jakiej daty należy sprawdzić pogodę. Data musi byc w formacie YYYY-mm-dd, np. 2022-11-03. W przypadku nie podania daty, aplikacja przyjmie za poszukiwaną datę następny dzień.
Aplikacja wykona zapytanie do API w celu poszukiwania stanu pogody.
Istnieją trzy możliwe informacje dla opadów deszczu:
Będzie padać (dla wyniku większego niż 0.0)
Nie będzie padać (dla wyniku równego 0.0)
Nie wiem (gdy wyniku z jakiegoś powodu nie ma lub wartość jest ujemna)
Będzie padać
Nie będzie padać
Nie wiem
Wyniki zapytań powinny być zapisywane do pliku. Jeżeli szukana data znajduje sie juz w pliku, nie wykonuj zapytania do API, tylko zwróć wynik z pliku.

URL do API:
https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}

W URL należy uzupełnić parametry: latitude, longitude oraz searched_date
'''

import json
from datetime import datetime, timedelta
import requests
from geopy.geocoders import Nominatim

API_URL = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" \
          "&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"


def retrieve_data_from_api(latitude, longitude, searched_date):
    response = requests.get(API_URL.format(latitude=latitude, longitude=longitude, searched_date=searched_date))
    data = json.loads(response.text)
    return data


def find_coordinates_for_city(city):
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude



def check_raining_sum(data: dict):
    raining_sum = data.get("daily").get("rain_sum")[0]
    if raining_sum > 0.0:
        return "Bedzie padać"
    elif raining_sum == 0.0:
        return "Nie bedzie padac"
    else:
        return "Nie wiem"


def read_data_from_file():
    with open("opady.txt", mode="a+") as file:
        data_in_file = file.read()
        return json.loads(data_in_file) if data_in_file else {}


def transform_data_in_file(data, city, date, raining_info):
    if data.get(city):
        data[city][date] = raining_info
    else:
        data[city] = {}
        data[city][date] = raining_info
    return json.dumps(data).replace("'", '"')


def write_data_to_file(data, city, date, raining_info):
    with open("opady.txt", mode="a+") as file:
        new_data = transform_data_in_file(data, city, date, raining_info)
        file.write(new_data)

def retrieve_data(file_data, city, date):
    city_data = file_data.get(city)
    if city_data:
        if city_data.get(date):
            return city_data[date], False
    latitude, longitude = find_coordinates_for_city(city)
    data = retrieve_data_from_api(latitude, longitude, date)
    raining_data = check_raining_sum(data)
    return raining_data, True

try:
    city = input("Podaj miasto, dla którego chcesz sprawdzić pogodę: ")
    date = input("Podaj datę, dla której chcesz sprawdzić pogodę: (YYYY-MM-DD)")
    if not date:
        date = datetime.now()
        date = date + timedelta(1)
        date = date.strftime('%Y-%m-%d')
        print("Nie podano daty, wyświetlono najbliższy dzień")
    data = read_data_from_file()
    raining_data, write_new_data_to_file = retrieve_data(data, city, date)
    if write_new_data_to_file:
        write_data_to_file(data, city, date, raining_data)
        print(data)
except: print("Nie znaleziono miasta lub podano datę w złym formacie")


#    print("Nie znaleziono miasta / Podano datę w złym formacie")