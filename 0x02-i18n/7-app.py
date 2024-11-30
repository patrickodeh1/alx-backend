#!/usr/bin/env python3
"""
Flask app with Babel, translations, user locale preferences, and timezone handling
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)

# Mock users database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """
    Configuration for Babel and Flask
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)
babel = Babel(app)

# Helper function to get user by ID
def get_user():
    """
    Get the user from the 'login_as' parameter.
    Returns a user dictionary or None if not found.
    """
    user_id = request.args.get('login_as', type=int)
    if user_id and user_id in users:
        return users[user_id]
    return None

# before_request function to set the user globally
@app.before_request
def before_request():
    """Set the user globally before every request."""
    user = get_user()
    g.user = user

@babel.localeselector
def get_locale():
    """
    Select the best language match based on client's request.
    Priority order:
    1. Locale from URL parameters
    2. Locale from user settings (if logged in)
    3. Locale from request header
    4. Default locale
    """
    # Step 1: Check for locale parameter in the URL
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # Step 2: Check user's locale from user settings
    if g.user and g.user['locale'] and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # Step 3: Check the request's Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES']) or app.config['BABEL_DEFAULT_LOCALE']

@babel.timezoneselector
def get_timezone():
    """
    Select the best timezone match based on client's request.
    Priority order:
    1. Timezone from URL parameters
    2. Timezone from user settings
    3. Default timezone (UTC)
    """
    # Step 1: Check for timezone parameter in the URL
    timezone = request.args.get('timezone')
    if timezone:
        try:
            # Validate the timezone using pytz
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            # If invalid timezone, fall back to default
            pass

    # Step 2: Check user's timezone from user settings
    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except UnknownTimeZoneError:
            pass

    # Step 3: Fall back to default timezone (UTC)
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    """Render the index template with translations and timezone info."""
    if g.user:
        welcome_msg = _("logged_in_as") % {"username": g.user["name"]}
    else:
        welcome_msg = _("not_logged_in")

    return render_template('7-index.html', welcome_msg=welcome_msg)

if __name__ == "__main__":
    app.run(debug=True)
