#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

from microservice2.broker_interface.generic_consumer import GenericConsumer
from microservice2.broker_interface.generic_producer import GenericProducer
from microservice2.open_weather.openweather_client import OpenWeatherClient

rabbitmq_host = os.environ.get(
    "AMQP_URL", "amqp://guest:guest@localhost?connection_attempts=5&retry_delay=5"
)
request_queue_name = "weatherUpdateRequest"
routing_key = "weatherUpdateRequest"
response_queue_name = "weatherUpdateResponse"
response_routing_key = "weatherUpdateResponse"
exchange_name = "weather_exchange"


class WeatherUpdatesHandler:
    connection = None

    def __init__(self):
        print(rabbitmq_host)
        self.weather_provider = OpenWeatherClient()
        self.consumer = GenericConsumer(
            rabbitmq_host,
            queue=request_queue_name,
            routing_key=routing_key,
            queue_durable=True,
            exchange=exchange_name,
        )
        self.producer = GenericProducer(
            rabbitmq_host,
            queue=response_queue_name,
            routing_key=response_routing_key,
            queue_durable=True,
            exchange=exchange_name,
        )

    def handle_weather_requests(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        request = json.loads(body)
        forecast = self.weather_provider.city_forecast(
            request["city_name"], request["country_code"]
        )
        if forecast is not None:
            self.producer.send_message(forecast.toJSON())

    def listen(self):
        self.consumer.listen(on_message_callback=self.handle_weather_requests)
