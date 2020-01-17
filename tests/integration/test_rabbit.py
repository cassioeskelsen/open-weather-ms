#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest
import requests
import time
from microservice1.broker_interface.generic_consumer import GenericConsumer
from microservice1.broker_interface.generic_producer import GenericProducer
from microservice1 import config
from microservice1.flask_app import create_app
from microservice1.forecast_storage.models import Forecast


class TestRabbit(unittest.TestCase):
    server_url = "http://localhost:5000/weather/v1.0/updateForecasts/{},{}"

    @classmethod
    def setUpClass(cls):

        rabbitmq_host = os.environ.get(
            "AMQP_URL",
            "amqp://guest:guest@localhost?connection_attempts=5&retry_delay=5",
        )
        request_queue_name = "testTopic"
        routing_key = "testRoutingKey"
        exchange_name = "test_exchange"

        cls.consumer = GenericConsumer(
            rabbitmq_host,
            queue=request_queue_name,
            routing_key=routing_key,
            queue_durable=True,
            exchange=exchange_name,
        )
        cls.producer = GenericProducer(
            rabbitmq_host,
            queue=request_queue_name,
            routing_key=routing_key,
            queue_durable=True,
            exchange=exchange_name,
        )

        cls.app = create_app(config=config.TestConfig)

    def test_send_message_rabbit(self):
        import uuid

        test_str = str(uuid.uuid4())
        TestRabbit.producer.send_message(test_str)
        return_from_broker = TestRabbit.consumer.get_next_message()
        self.assertEqual(return_from_broker.decode("utf-8"), test_str)

    def test_get_forecasts_for_remote_city(self):
        remote_city = "Yanjiao"  # prevent conflict with another manual tests with well knowledge cities
        remote_country = "CN"
        check_count = -1
        with TestRabbit.app.app_context():
            Forecast().delete_forecasts(remote_city, remote_country)
            check_count = len(Forecast().get_forecasts(remote_city, remote_country))
            self.assertEqual(check_count, 0, msg="Database was not reset")

            r = requests.get(self.server_url.format(remote_city, remote_country))
            self.assertEqual(r.status_code, 200)

            print("wait 3 seconds...")

            time.sleep(3)

            check_count = len(Forecast().get_forecasts(remote_city, remote_country))
            self.assertEqual(
                check_count, 5, msg="No records were registered for the city"
            )

    @classmethod
    def tearDownClass(cls):
        cls.producer.close()
        cls.consumer.close()
