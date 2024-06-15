import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH2_CLIENT_ID = 'myclient'
    OAUTH2_CLIENT_SECRET = 'client-secret-from-keycloak'
    OAUTH2_DISCOVERY_URL = 'http://localhost:8080/realms/myrealm/.well-known/openid-configuration'
