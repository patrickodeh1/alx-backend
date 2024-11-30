#!/usr/bin/env python3
"""
Flask app with Babel and translations
This Flask application demonstrates
internationalization (i18n) using Flask-Babel.
It supports two languages: English and French. The app serves a homepage with
translations based on the user's language preference.
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)


class Config:
    """
    Configuration class for the Flask app and Flask-Babel.

    Attributes:
        LANGUAGES (list): List of supported languages for translation.
        BABEL_DEFAULT_LOCALE (str): The default locale for the app (English).
        BABEL_DEFAULT_TIMEZONE (str): The default timezone for the app (UTC).
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Select the best language match based on client's request.
    If the 'locale' query parameter is passed, use that locale if valid.
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the index template with translations.
    This route renders the homepage with a title and header
    that are translated based
    on the current locale. The title and header texts
    are retrieved using the `_()`
    function for translation.
    """
    return render_template('4-index.html',
                           title=_("home_title"),
                           header=_("home_header"))


if __name__ == "__main__":
    app.run(debug=True)
