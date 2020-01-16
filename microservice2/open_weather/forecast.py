#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from microservice2.open_weather.daily_forecast import DailyForecast


class Forecast:
    """
        Commom forecast object to isolate broker from provider forecast format
    """

    def __init__(self, city_name, country_code):
        self.city_name = city_name
        self.country_code = country_code
        self.daily_forecasts = []

    def append_daily_forecast(
        self,
        datetime: int,
        temp_max: float,
        temp_min: float,
        temp_day: float,
        feels_like_day: float,
        humidity: float,
        weather_id: int,
        weather_description: str,
    ):
        """
                :param datetime: datetime unix format
                :param temp_max: max daily temperature
                :param temp_min: min daily temperature
                :param temp_day: day temperature
                :param feels_like_day: human perception temperature
                :param humidity: % humidity
                :param weather_id: weather condition code
                :param weather_description: human readable description
        """
        self.daily_forecasts.append(
            DailyForecast(
                datetime=datetime,
                temp_max=temp_max,
                temp_min=temp_min,
                temp_day=temp_day,
                feels_like_day=feels_like_day,
                humidity=humidity,
                weather_id=weather_id,
                weather_description=weather_description,
            )
        )

    def toJSON(self):
        return json.dumps(
            self, default=lambda obj: obj.__dict__
        )  # , sort_keys=True, indent=4)
