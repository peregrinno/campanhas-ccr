import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_URL', 'mysql+mysqlconnector://user_ccr:#ccr-apps#@localhost/ccr_campanhas')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
