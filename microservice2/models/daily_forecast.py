#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import dumps, JSONEncoder


class DailyForecast:
    """
    Commom forecast object to isolate broker from provider forecast format
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def toJSON(self):
        class DailyForecastEncoder(JSONEncoder):
            def default(self, o):
                return o.__dict__

        return dumps(self, cls=DailyForecastEncoder)
