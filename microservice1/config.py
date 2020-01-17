#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = ""


class DevelopmentConfig(BaseConfig):
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    database = os.environ["POSTGRES_DB"]
    port = os.environ["POSTGRES_PORT"]
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{ user}:{password}@{host}:{port}/{database}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = "localhost"
    database = os.environ["POSTGRES_DB"]
    port = os.environ["POSTGRES_PORT"]
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
