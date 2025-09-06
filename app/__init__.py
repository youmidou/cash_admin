from flask import Flask
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 注册蓝图
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
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
    
    from app.system import bp as system_bp
    app.register_blueprint(system_bp, url_prefix='/system')
    
    from app.reward import bp as reward_bp
    app.register_blueprint(reward_bp, url_prefix='/reward')
    
    from app.cheat import bp as cheat_bp
    app.register_blueprint(cheat_bp, url_prefix='/cheat')
    
    from app.jackpot import bp as jackpot_bp
    app.register_blueprint(jackpot_bp, url_prefix='/jackpot')
    
    from app.report import bp as report_bp
    app.register_blueprint(report_bp, url_prefix='/report')
    
    from app.broadcast import bp as broadcast_bp
    app.register_blueprint(broadcast_bp, url_prefix='/broadcast')
    
    from app.stamps import bp as stamps_bp
    app.register_blueprint(stamps_bp, url_prefix='/stamps')

    from app.quest import bp as quest_bp
    app.register_blueprint(quest_bp, url_prefix='/quest')
    
    return app
