#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = ""


class DevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
