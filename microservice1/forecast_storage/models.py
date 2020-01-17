#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask_sqlalchemy
from datetime import datetime

db = flask_sqlalchemy.SQLAlchemy(session_options={"expire_on_commit": False})


class Forecast(db.Model):
    __tablename__ = "forecast"
    id = db.Column(
        db.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True
    )
    city_name = db.Column(db.String(50), nullable=False, index=True)
    country_code = db.Column(db.String(5), nullable=False)
    timestamp = db.Column(db.Float, index=True)
    temp_max = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    temp_day = db.Column(db.Float)
    feels_like_day = db.Column(db.Float)
    humidity = db.Column(db.Float)
    weather_id = db.Column(db.Integer)
    weather_description = db.Column(db.String(50))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_forecast_by_id(id):
        return Forecast.query.get(id)

    @staticmethod
    def get_or_new(_city_name, _country_code, _datetime):
        instance = Forecast.query.filter_by(
            city_name=_city_name, country_code=_country_code, timestamp=_datetime
        ).first()
        if instance:
            return instance
        else:
            return Forecast()

    def getDate(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%d/%m/%Y")

    def __repr__(self):
        str = "{},{} - {} - Minima:{}°C - Maxima:{}°C - Temp Dia:{}°C - Sensação Térmica:{}°C - Previsão:{}"
        return str.format(
            self.city_name,
            self.country_code,
            self.getDate(),
            self.temp_min,
            self.temp_max,
            self.temp_day,
            self.feels_like_day,
            self.weather_description,
        )
