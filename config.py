import os

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    MONGODB_HOST='mongodb://admin:admin1@ds259255.mlab.com:59255/cinder'
    MONGODB_DB='cinder'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
