import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_URL', 'mysql://root:zoW-X[]IwbWw*_C9@localhost/ccr_campanhas')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
