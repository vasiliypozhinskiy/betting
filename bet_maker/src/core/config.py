import os
from logging import config as logging_config

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'bet_maker')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_HOST = os.getenv('DB_HOST')