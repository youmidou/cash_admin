from flask import Flask
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 注册蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    
    from app.theme import bp as theme_bp
    app.register_blueprint(theme_bp, url_prefix='/theme')
    
    from app.config import bp as config_bp
    app.register_blueprint(config_bp, url_prefix='/config')
    
    from app.activity import bp as activity_bp
    app.register_blueprint(activity_bp, url_prefix='/activity')
    
    return app
