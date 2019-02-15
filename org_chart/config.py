import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False
    TESTING = False

    LOGGING_FORMAT = '%(asctime)s [%(levelname)s:%(funcName)s:%(lineno)d] %(message)s'
    LOGGING_LOCATION = 'logs/org_chart.log' #'org_chart.log'
    LOGGING_MAXBYTES = 10240
    LOGGING_BACKUPCOUNT = 10

    LOGGING_LEVEL = logging.DEBUG

