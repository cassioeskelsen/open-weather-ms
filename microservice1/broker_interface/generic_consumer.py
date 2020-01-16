#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pika
import pika.exceptions


class GenericConsumer(object):
    def __init__(
        self,
        amqp_url,
        queue,
        routing_key="message",
        exchange="message",
        exchange_type="topic",
        queue_durable=False,
    ):
        self.exchange_name = exchange
        self.exchange_type = exchange_type
        self.queue_name = queue
        self.routing_key_name = routing_key
        self.queue_durable = queue_durable
        self._connection = None
        self._channel = None
        self._url = amqp_url

        self.open_connection()
        self.setup_channel()

    def open_connection(self):
        parameters = pika.URLParameters(self._url)
        self._connection = pika.BlockingConnection(parameters)
        # self._connection = pika.BlockingConnection(
        #    pika.ConnectionParameters(
        #        host="rabbitmq", connection_attempts=5, retry_delay=5
        #    )
        # )

    def setup_channel(self):
        channel = self._connection.channel()
        channel.exchange_declare(
            exchange=self.exchange_name, exchange_type=self.exchange_type
        )
        channel.queue_declare(queue=self.queue_name, durable=self.queue_durable)
        channel.queue_bind(
            exchange=self.exchange_name,
            queue=self.queue_name,
            routing_key=self.routing_key_name,
        )
        self._channel = channel

    def listen(self, on_message_callback):
        self.open_connection()
        self._channel.basic_consume(
            on_message_callback=on_message_callback, queue=self.queue_name,
        )
        try:
            self._channel.start_consuming()
        except pika.exceptions.StreamLostError:
            self.listen(on_message_callback=on_message_callback)
        except KeyboardInterrupt:
            self._connection.close()

    def close(self):
        self._connection.close()
