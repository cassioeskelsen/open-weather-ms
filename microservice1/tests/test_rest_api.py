#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import requests


class RestAPITest(unittest.TestCase):

    server_url = "http://localhost:5000{}"

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
