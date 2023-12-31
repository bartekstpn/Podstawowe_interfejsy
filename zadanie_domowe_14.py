from praca_domowa_14.Weather_Forecast import WeatherForecast

try:
    def run_program(weather_forecast: WeatherForecast):
        weather_info, write_to_file = weather_forecast.retrieve_data()
        weather_forecast.write_data_to_file(weather_info)

    weather_forecast = WeatherForecast()
    run_program(weather_forecast)

    for item in weather_forecast.items():
        print(item)
except TypeError:
    print("Coś poszło nie tak")