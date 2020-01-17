#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import requests
import time

from microservice1 import config
from microservice1.flask_app import create_app
from microservice1.forecast_storage.models import Forecast

server_url = "http://localhost:5000/weather/v1.0/updateForecasts/{}"
app = create_app(config=config.TestConfig)


def help():
    print("weather.py -r <city,country code>: request forecast to OpenWeather ")
    print("weather.py -l <city,country code>: list forecast ")
    print("\nexample:")
    print("weather.py -r Blumenau,BR")
    print("weather.py -l Blumenau,BR")
    print("\nweather.py -h show this help ")


def request_forecast(city_name, list=False):
    r = requests.get(server_url.format(city_name))
    if r.status_code == 200:
        print("OK")
        if list:
            time.sleep(1)
            list_forecast(city_name)
    else:
        print("Error")


def list_forecast(city_name):
    country_code = "BR"
    if "," in city_name:
        country_code = city_name.split(",")[1]
        city_name = city_name.split(",")[0]
    with app.app_context():
        forecasts = Forecast().get_forecasts(city_name, country_code)
        for f in forecasts:
            print(str(f))


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hr:l:s:", ["rcity=", "lcity=", "scity="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            help()
            sys.exit()
        elif opt in ("-r", "--rcity"):
            request_forecast(arg)
        elif opt in ("-l", "--lcity"):
            list_forecast(arg)
        elif opt in ("-s", "--scity"):
            request_forecast(arg, list=True)


if __name__ == "__main__":
    main(sys.argv[1:])
