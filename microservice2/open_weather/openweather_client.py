#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests

from microservice2.models.forecast import Forecast


class OpenWeatherClient:
    def __init__(self):
        self.api_key = os.getenv("OWMAPI")
        if self.api_key is None:
            raise Exception("OpenWeather API KEY is not defined")

    def city_forecast(
        self, city_name, country_code="BR", days_forecast=5, lang="pt_BR"
    ):
        """
        Get <days_forecast> for <city_name>
        :param city_name:
        :param country_code: ISO 3166 country code.
        :param days_forecast: number of days to get forecast from OWM
        :return:
        """

        url = (
            "http://api.openweathermap.org/data/2.5/forecast/daily?q={},{}&mode=json&units=metric&cnt={}"
            "&units=metric&appid={}&lang={}"
        )

        try:
            res = requests.get(
                url.format(city_name, country_code, days_forecast, self.api_key, lang)
            )

            j = res.json()
            f = Forecast(city_name=j["city"]["name"], country_code=j["city"]["country"])

            for d in j["list"]:
                f.append_daily_forecast(
                    datetime=d["dt"],
                    temp_max=float(d["temp"]["max"]),
                    temp_min=float(d["temp"]["min"]),
                    temp_day=float(d["temp"]["day"]),
                    feels_like_day=float(d["feels_like"]["day"]),
                    humidity=float(d["humidity"]),
                    weather_id=int(d["weather"][0]["id"]),
                    weather_description=d["weather"][0]["description"],
                )
            return f
        except Exception:
            # generic error handling for now
            return None
