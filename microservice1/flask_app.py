#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from microservice1.forecast_storage.models import db
from . import config


def create_app(config=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    app.app_context().push()
    db.init_app(app)
    db.create_all()

    return app
