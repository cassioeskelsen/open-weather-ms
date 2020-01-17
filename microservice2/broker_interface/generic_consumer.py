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

    def get_next_message(self, max_retry=5):
        """

        :param max_retry: max attempts to get messages. One second interval between attempts.
        :return: message or None
        """
        from time import sleep

        retry_count = 0

        self.open_connection()

        while True:
            method, property, body = self._channel.basic_get(
                queue=self.queue_name, auto_ack=True
            )
            if body:
                return body
            else:
                if retry_count < max_retry:
                    sleep(1)
                else:
                    return None

    def close(self):
        self._connection.close()
