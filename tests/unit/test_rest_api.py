#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import requests
from microservice1 import config
from microservice1.app import app


class RestAPITest(unittest.TestCase):

    server_url = "http://localhost:5000{}"

    def setUp(self):
        app.config.from_object(config.TestConfig)
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False

        # Setting test client
        self.app = app.test_client()
        self.app.testing = True

    def test_request_weather_city_and_coutry(self):
        r = requests.get(
            self.server_url.format("/weather/v1.0/updateForecasts/Blumenau,BR")
        )
        self.assertEqual(r.status_code, 200)

    def test_request_weather_city(self):
        r = requests.get(
            self.server_url.format("/weather/v1.0/updateForecasts/Blumenau")
        )
        self.assertEqual(r.status_code, 200)

    def test_request_weather_without_parameters_should_return_400(self):
        r = requests.get(self.server_url.format("/weather/v1.0/updateForecasts"))
        self.assertEqual(r.status_code, 404)
