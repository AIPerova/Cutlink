from datetime import datetime
import random
import re
from validators import url

from flask import url_for

from yacut import db
from .error_handlers import ShortGenerateError, URLValidateError
from .constans import (VALID_SHORT_SYMBOLS,
                       VALID_SHORT_PATTERN,
                       ORIGINAL_URL_LENGHT,
                       SHORT_URL_LENGHT,
                       RANDOM_SHORT_LENGHT)


class URLMap(db.Model):
    """Модель конвертера ссылок. """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_LENGHT), nullable=False)
    short = db.Column(db.String(SHORT_URL_LENGHT), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def generate_short():
        """Метод создания рандомной короткой ссылки."""
        short_id = ''.join(random.choices(VALID_SHORT_SYMBOLS, k=RANDOM_SHORT_LENGHT))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id

    @staticmethod
    def save(original, short):
        """Метод сохранения ссылки в БД."""
        if not url(original):
            raise URLValidateError("Некорректный url!")
        if short:
            if URLMap.query.filter_by(short=short).first():
                raise ShortGenerateError()
            if len(short) > SHORT_URL_LENGHT:
                raise URLValidateError("Указано недопустимое имя для короткой ссылки")
            if not re.match(VALID_SHORT_PATTERN, short):
                raise URLValidateError("Указано недопустимое имя для короткой ссылки")

        else:
            short = URLMap.generate_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        """Преобразование объекта в словарь."""
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_link', short=self.short, _external=True
            )
        )
