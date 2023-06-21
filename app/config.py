# config.py

class Config:
    SECRET_KEY = 'my-super-duper-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    UPLOAD_FOLDER = 'app/static/data'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'
    TESTING = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/mydatabase'
    DEBUG = False
