from os import getenv

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
