import os
import unittest
import json

from microservice2.open_weather.openweather_client import OpenWeatherClient


class SetupTest(unittest.TestCase):
    def test_api_key_from_environment(self):
        owc = OpenWeatherClient()
        self.assertEqual(owc.api_key, os.getenv("OWMAPI"))

    def test_serialize_daily_forecast(self):
        test = {
            "datetime": 1579186800,
            "temp_max": 38.0,
            "temp_min": 28.0,
            "temp_day": 35.0,
            "feels_like_day": 40.0,
            "humidity": 60.0,
            "weather_id": 801,
            "weather_description": "poucas nuvens",
        }

        from microservice2.open_weather.daily_forecast import DailyForecast

        f = DailyForecast(
            datetime=1579186800,
            temp_max=38,
            temp_min=28,
            temp_day=35,
            feels_like_day=40,
            humidity=60,
            weather_id=801,
            weather_description="poucas nuvens",
        )
        t = json.loads(f.toJSON())
        self.assertEqual(test, t)

    def test_owm_api_city_should_be_blumenau(self):
        owc = OpenWeatherClient()
        f = owc.city_forecast(city_name="Blumenau")
        self.assertEqual(f.city_name, "Blumenau")
        self.assertEqual(f.country_code, "BR")

    def test_owm_api_forecasts_should_be_five(self):
        owc = OpenWeatherClient()
        f = owc.city_forecast(city_name="São Paulo")
        self.assertEqual(len(f.daily_forecasts), 5)
