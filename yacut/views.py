from flask import redirect, render_template, flash, url_for

from . import app
from .error_handlers import ShortGenerateError
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Генерация новой короткой ссылки."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)

    try:
        url_map = URLMap.save(
            original=form.original_link.data,
            short=form.custom_id.data,
        )
    except ShortGenerateError:
        flash("Предложенный вариант короткой ссылки уже существует.")
        flash('Имя "{}" уже занято.'.format(form.custom_id.data))
        return render_template("index.html", form=form)
    return (
        render_template(
            "index.html",
            form=form,
            short_link=url_for(
                'redirect_link',
                short=url_map.short,
                _external=True,
            ),
        ),
        200,
    )


@app.route('/<short>')
def redirect_link(short):
    """Перенаправление на оригинальный url."""
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )