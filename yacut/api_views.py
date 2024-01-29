from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import (
    InvalidAPIUsageError,
    URLValidateError,
    ShortGenerateError
)
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_link():
    """Создание короткой ссылки API."""
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsageError("Отсутствует тело запроса")
    original = data.get('url')
    if not original:
        raise InvalidAPIUsageError('\"url\" является обязательным полем!')
    custom_id = data.get('custom_id')
    try:
        return (jsonify(
            URLMap.save(original, custom_id).to_dict()
        ), 201)
    except URLValidateError as error:
        raise InvalidAPIUsageError(str(error))
    except ShortGenerateError:
        raise InvalidAPIUsageError("Предложенный вариант короткой ссылки уже существует.")


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original_url(short):
    """Переадресация на первоначальный URL API."""
    url_map = URLMap.query.filter_by(short=short).first()
    if not url_map:
        raise InvalidAPIUsageError(
            'Указанный id не найден', HTTPStatus.NOT_FOUND
        )
    return (jsonify({'url': url_map.original}), HTTPStatus.OK)
