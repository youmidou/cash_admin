from flask import render_template, request, jsonify, flash, redirect, url_for
from app.config import bp
from app.api_client import GameServerAPI

@bp.route('/')
def config_list():
    """配置管理主页"""
    return render_template('config/list.html')

@bp.route('/daily', methods=['GET', 'POST'])
def daily_config():
    """每日配置管理"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        config_data = {
            'daily_bonus': {
                'enabled': request.form.get('daily_bonus_enabled') == 'on',
                'amount': int(request.form.get('daily_bonus_amount', 0))
            },
            'wheel_spin': {
                'enabled': request.form.get('wheel_spin_enabled') == 'on',
                'cost': int(request.form.get('wheel_spin_cost', 0))
            },
            'ad_rewards': {
                'enabled': request.form.get('ad_rewards_enabled') == 'on',
                'multiplier': float(request.form.get('ad_rewards_multiplier', 1.0))
            }
        }
        
        result = api.set_daily_config(config_data)
        
        if result.get('error'):
            flash(f'更新每日配置失败: {result["error"]}', 'error')
        else:
            flash('每日配置更新成功', 'success')
    
    # 获取当前配置
    config_info = api.get_daily_config()
    
    return render_template('config/daily.html', config_info=config_info)

@bp.route('/activity', methods=['GET', 'POST'])
def activity_config():
    """活动配置管理"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        config_data = {
            'events': {
                'enabled': request.form.get('events_enabled') == 'on',
                'duration': int(request.form.get('events_duration', 7))
            },
            'tournaments': {
                'enabled': request.form.get('tournaments_enabled') == 'on',
                'frequency': request.form.get('tournaments_frequency', 'weekly')
            },
            'special_offers': {
                'enabled': request.form.get('special_offers_enabled') == 'on',
                'discount': float(request.form.get('special_offers_discount', 0.0))
            }
        }
        
        result = api.set_activity_config(config_data)
        
        if result.get('error'):
            flash(f'更新活动配置失败: {result["error"]}', 'error')
        else:
            flash('活动配置更新成功', 'success')
    
    # 获取当前配置
    config_info = api.get_activity_config()
    
    return render_template('config/activity.html', config_info=config_info)

@bp.route('/ac', methods=['GET', 'POST'])
def ac_config():
    """AC配置管理"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        config_data = {
            'artificial_control': {
                'enabled': request.form.get('ac_enabled') == 'on',
                'level': request.form.get('ac_level', 'normal')
            },
            'win_rate': {
                'min': float(request.form.get('win_rate_min', 0.85)),
                'max': float(request.form.get('win_rate_max', 0.95))
            },
            'jackpot': {
                'enabled': request.form.get('jackpot_enabled') == 'on',
                'frequency': int(request.form.get('jackpot_frequency', 1000))
            }
        }
        
        result = api.set_ac_config(config_data)
        
        if result.get('error'):
            flash(f'更新AC配置失败: {result["error"]}', 'error')
        else:
            flash('AC配置更新成功', 'success')
    
    # 获取当前配置
    config_info = api.get_ac_config()
    
    return render_template('config/ac.html', config_info=config_info)

@bp.route('/system')
def system_config():
    """系统配置页面"""
    api = GameServerAPI()
    system_info = api.get_system_info()
    
    return render_template('config/system.html', system_info=system_info)
