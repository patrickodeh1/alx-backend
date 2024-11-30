#!/usr/bin/env python3
"""
Flask app with Babel, translations, and mock user login
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    Configuration for Babel
    Flask
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


def get_user():
    """
    Get the user from the 'login_as' parameter.
    Returns a user dictionary or None if not found.
    """
    user_id = request.args.get('login_as', type=int)
    if user_id and user_id in users:
        return users[user_id]
    return None


@app.before_request
def before_request():
    """Set the user globally before every request."""
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """
    Select the best language match based on client's request.
    If the 'locale' query parameter is passed, use that locale if valid.
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the index template with translations."""
    if g.user:
        welcome_msg = _("logged_in_as") % {"username": g.user["name"]}
    else:
        welcome_msg = _("not_logged_in")
    return render_template('5-index.html', welcome_msg=welcome_msg)


if __name__ == "__main__":
    app.run(debug=True)
