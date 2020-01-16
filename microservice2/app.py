#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from microservice2.weather_updates_handler import WeatherUpdatesHandler

if __name__ == "__main__":
    wuh = WeatherUpdatesHandler()
    print("Starting Microservice2...")
    wuh.listen()
