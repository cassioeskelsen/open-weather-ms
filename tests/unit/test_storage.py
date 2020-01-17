#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from microservice1 import config
from microservice1.flask_app import create_app
from microservice1.forecast_storage.models import Forecast


class SetupTest(unittest.TestCase):
    def setUp(self):
        app = create_app(config=config.TestConfig)
        self.app = app

    def get_basic_object(self):
        forecast = Forecast()
        forecast.timestamp = 1579221779
        forecast.city_name = "Blumenau"
        forecast.country_code = "BR"
        forecast.temp_max = 30.0
        forecast.temp_min = 31.0
        forecast.temp_min = 25.0
        forecast.temp_day = 28.0
        forecast.feels_like_day = 35
        forecast.humidity = 80.0
        forecast.weather_description = "chuva leve"
        return forecast

    def test_basic_model(self):
        expected_string = (
            "Blumenau,BR - 16/01/2020 - Minima:25.0°C - Maxima:30.0°C - Temp Dia:28.0°C "
            "- Sensação Térmica:35°C - Previsão:chuva leve"
        )
        self.assertEqual(str(self.get_basic_object()), expected_string)

    def test_save_forecast(self):
        with self.app.app_context():
            forecast = self.get_basic_object()
            forecast.save()
