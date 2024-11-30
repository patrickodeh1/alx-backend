#!/usr/bin/env python3
"""
Flask app with Babel and translations.

This Flask application demonstrates
internationalization (i18n) using Flask-Babel.
It supports two languages: English and French. The app serves a homepage with
translations based on the user's language preference.

Configuration:
    - LANGUAGES: List of supported languages (English and French).
    - BABEL_DEFAULT_LOCALE: Default locale for the app (English).
    - BABEL_DEFAULT_TIMEZONE: Default timezone for the app (UTC).

"""

from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)

babel = Babel(app)


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
    Select the best language match based on the client's request.

    This function checks the 'Accept-Language' header sent
    by the client and selects

    Returns:
        str: The best matching language from the list of supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """
    Render the index template with translated strings.

    This route renders the homepage with a title and header
    that are translated based
    on the current locale. The title and header texts
    are retrieved using the `_()`
    function for translation.

    Returns:
        Response: The rendered HTML page, with the translated title and header.
    """
    return render_template('3-index.html')

if __name__ == "__main__":
    app.run(debug=True)
