#
# @author    Matthias Genzmehr
# @copyright 2024 Universitätsbibliothek Mainz
# @version   1.0
#

from flask import Flask, request
from flask_babel import Babel
from theapp.logic.requestform import requestform

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config['BABEL_DEFAULT_LOCALE'] = 'de'

app.register_blueprint(requestform)

def get_locale():
    if request.form.get('language') and request.form.get('language') in ['de', 'en']:
        return request.form.get('language')
    
    if request.args.get('lng') and request.args.get('lng') in ['de', 'en']:
        return request.args.get('lng')
    
    return 'de'

babel = Babel(app, locale_selector=get_locale)

#
# Prepare Logging
#

import logging
from logging import FileHandler, Formatter
from logging.handlers import TimedRotatingFileHandler

app.logger.setLevel(logging.INFO)

# Session Logging

class InfoOnlyFilter(logging.Filter):
    def filter(self, record):
        if record.levelname == "INFO":
            return True
        return False

session_log_handler = FileHandler(app.config['SESSION_LOG'])
session_log_handler.setLevel(logging.INFO)
session_log_handler.addFilter(InfoOnlyFilter())
session_log_handler.setFormatter(Formatter(
                            "{asctime} {levelname}: {message}",
                            "%Y-%m-%d %H:%M:%S",
                            style="{"))

app.logger.addHandler(session_log_handler)

# Error Logging

error_log_handler = FileHandler(app.config['ERROR_LOG'])
error_log_handler.setLevel(logging.ERROR)
error_log_handler.setFormatter(Formatter(
                            "{asctime} {levelname}: {message}",
                            "%Y-%m-%d %H:%M:%S",
                            style="{"))

app.logger.addHandler(error_log_handler)

# Debug Logging

if app.debug == True:
    app.logger.setLevel(logging.DEBUG)

    debug_log_handler = FileHandler(app.config['DEBUG_LOG'])
    debug_log_handler.setLevel(logging.DEBUG)
    debug_log_handler.setFormatter(Formatter(
                            "{asctime} {levelname}: {message}",
                            "%Y-%m-%d %H:%M:%S",
                            style="{"))

    app.logger.addHandler(debug_log_handler)
