from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
# from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from app import routes, models

# handler = logging.FileHandler(app.config['LOGGING_LOCATION'])

handler = RotatingFileHandler(app.config['LOGGING_LOCATION'],
                              maxBytes=app.config['LOGGING_MAXBYTES'],
                              backupCount=app.config['LOGGING_BACKUPCOUNT'])

handler.setLevel(app.config['LOGGING_LEVEL'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)