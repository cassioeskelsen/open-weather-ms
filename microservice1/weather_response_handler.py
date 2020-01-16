#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from time import sleep

import threading

from microservice1.broker_interface.generic_consumer import GenericConsumer

rabbitmq_host = os.environ.get(
    "AMQP_URL", "amqp://guest:guest@localhost?connection_attempts=5&retry_delay=5"
)
response_queue_name = "weatherUpdateResponse"
response_routing_key = "weatherUpdateResponse"
exchange_name = "weather_exchange"


class WeatherResponseHandler:
    connection = None
    internal_lock = threading.Lock()

    def __init__(self):
        self.consumer = GenericConsumer(
            rabbitmq_host,
            queue=response_queue_name,
            routing_key=response_routing_key,
            queue_durable=True,
            exchange=exchange_name,
        )

    def handle_weather_requests(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # request = json.loads(body)
        print(body)

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
