from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from .constans import (VALID_SHORT_PATTERN,
                       ORIGINAL_URL_LENGHT,
                       SHORT_URL_LENGHT)


class URLMapForm(FlaskForm):
    """Форма для конвертации ссылок."""
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, ORIGINAL_URL_LENGHT),
                    URL(require_tld=True, message='Введите корректный url!')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, SHORT_URL_LENGHT),
                    Regexp(VALID_SHORT_PATTERN),
                    Optional()]
    )
    submit = SubmitField('Создать')
