#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from time import sleep

import threading

from microservice1.broker_interface.generic_consumer import GenericConsumer
from microservice1.forecast_storage.models import Forecast

rabbitmq_host = os.environ.get(
    "AMQP_URL", "amqp://guest:guest@localhost?connection_attempts=5&retry_delay=5"
)
response_queue_name = "weatherUpdateResponse"
response_routing_key = "weatherUpdateResponse"
exchange_name = "weather_exchange"


class WeatherResponseHandler:
    connection = None
    internal_lock = threading.Lock()

    def __init__(self, app_context):
        self.consumer = GenericConsumer(
            rabbitmq_host,
            queue=response_queue_name,
            routing_key=response_routing_key,
            queue_durable=True,
            exchange=exchange_name,
        )

        self.database_context = app_context

    def handle_weather_requests(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        received = json.loads(body)
        for r in received["daily_forecasts"]:
            print(r)
            with self.database_context.app_context():
                f = Forecast().get_or_new(
                    received["city_name"], received["country_code"], r["datetime"]
                )
                f.city_name = received["city_name"]
                f.country_code = received["country_code"]
                f.timestamp = r["datetime"]
                f.temp_min = float(r["temp_min"])
                f.temp_max = float(r["temp_max"])
                f.temp_day = float(r["temp_day"])
                f.feels_like_day = float(r["temp_day"])
                f.humidity = float(r["humidity"])
                f.weather_id = int(r["weather_id"])
                f.weather_description = r["weather_description"]
                f.save()

    def listen(self):
        self.consumer.listen(on_message_callback=self.handle_weather_requests)
        while True:
            with self.internal_lock:
                self.connection.process_data_events()
                sleep(0.1)

    def start(self):
        thread = threading.Thread(target=self.listen)
        thread.setDaemon(True)
        thread.start()
