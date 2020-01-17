#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from flask import g
from microservice1.broker_interface.generic_producer import GenericProducer
from microservice1.flask_app import create_app
from microservice1.weather_response_handler import WeatherResponseHandler

app = create_app()

rabbitmq_host = os.environ.get(
    "AMQP_URL", "amqp://guest:guest@localhost?connection_attempts=5&retry_delay=5"
)
request_queue_name = "weatherUpdateRequest"
routing_key = "weatherUpdateRequest"
exchange_name = "weather_exchange"


def get_broker():
    if not hasattr(g, "broker"):
        g.broker = GenericProducer(
            rabbitmq_host,
            queue=request_queue_name,
            routing_key=routing_key,
            queue_durable=True,
            exchange=exchange_name,
        )
    return g.broker


@app.teardown_appcontext
def close_queue(error):
    if hasattr(g, "broker"):
        g.broker.close()


@app.route("/weather/v1.0/updateForecasts/<city_name>")
def update_forecast(city_name):
    country_code = "BR"
    if "," in city_name:
        country_code = city_name.split(",")[1]
        city_name = city_name.split(",")[0]

    print(country_code + " -  " + city_name)

    request = {"city_name": city_name, "country_code": country_code}
    try:
        get_broker().send_message(json.dumps(request))
    except:
        return "", 503
    return "", 200


if __name__ == "__main__":
    with app.app_context():
        wrh = WeatherResponseHandler(app)
        wrh.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
