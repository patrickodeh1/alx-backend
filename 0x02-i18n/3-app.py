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

Routes:
    - /: Home page, where the app displays a translated
    itle and header based on the selected locale.

Translation Files:
    - The translations are stored in the 'translations' directory and include
      'messages.po' and 'messages.mo' files for the supported languages.

Usage:
    - To run the app, make sure to have Flask and Flask-Babel installed.
    - Run the app using `python3 app.py` and
    access the page to see translations based on the browser's
    language preferences.

Dependencies:
    - Flask: A lightweight WSGI web application framework.
    - Flask-Babel: Adds i18n and l10n support to Flask.

Example:
    - If the browser prefers French, the app will display
    the translated version of the title and header.
    - If French is not available, the app will fall back to English.
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
    Select the best language match based on the client's request.

    This function checks the 'Accept-Language' header sent
    by the client and selects
    the most appropriate language from
    the list of supported languages. If the client
    requests a language that isn't supported,
    it falls back to the default language.

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
    return render_template('3-index.html',
                           title=_("home_title"),
                           header=_("home_header"))


if __name__ == "__main__":
    app.run(debug=True)
