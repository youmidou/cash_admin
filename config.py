import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    GAME_SERVER_HOST = os.environ.get('GAME_SERVER_HOST') or 'localhost'
    GAME_SERVER_PORT = int(os.environ.get('GAME_SERVER_PORT') or '5001')
    GAME_SERVER_ADMIN_KEY = os.environ.get('GAME_SERVER_ADMIN_KEY') or 'admin_key_20250906'
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
