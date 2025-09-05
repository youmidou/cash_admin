import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    GAME_SERVER_URL = os.environ.get('GAME_SERVER_URL') or 'http://localhost:5000'
    GAME_SERVER_ADMIN_KEY = os.environ.get('GAME_SERVER_ADMIN_KEY') or 'admin-key'
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
