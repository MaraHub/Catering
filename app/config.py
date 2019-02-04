## Imports
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Auth:
    CLIENT_ID = ('1009864485884-bo8l1jhl6mk8v21ltlp6qqnj4q7p9kcj.apps.googleusercontent.com')
    CLIENT_SECRET = 'tXyY4pZktAuVxflrZSltgFDv'
    REDIRECT_URI = 'https://localhost:5000/google_login'
    REQUEST_AUTHORIZATION = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/oauth2/v1/userinfo'
    SCOPE = ['https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile']

class Config:
    APP_NAME = "dinebeat"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aajlm1981#@localhost/catering_db'

class DevConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "test.db")


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "prod.db")


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
