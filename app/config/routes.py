from flask import render_template, request, jsonify, flash, redirect, url_for
from app.config import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
@login_required
def config_management():
    """配置管理主页面"""
    return render_template('config/management.html')

@bp.route('/daily')
@login_required
def daily_config():
    """每日配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_daily_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('config/daily.html', config_data=config_data)
        else:
            flash(f'获取每日配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('config.config_management'))
    except Exception as e:
        flash(f'获取每日配置失败: {str(e)}', 'error')
        return redirect(url_for('config.config_management'))

@bp.route('/daily', methods=['POST'])
@login_required
def update_daily_config():
    """更新每日配置"""
    api = GameServerAPI()
    try:
        # 获取表单数据
        config_data = {
            'daily_bonus': {
                'enabled': request.form.get('daily_bonus_enabled') == 'on',
                'base_coins': int(request.form.get('daily_bonus_base_coins', 0)),
                'multiplier': float(request.form.get('daily_bonus_multiplier', 1.0)),
                'max_days': int(request.form.get('daily_bonus_max_days', 7))
            },
            'daily_mission': {
                'enabled': request.form.get('daily_mission_enabled') == 'on',
                'reset_time': request.form.get('daily_mission_reset_time', '00:00:00'),
                'missions_per_day': int(request.form.get('daily_mission_count', 3)),
                'reward_multiplier': float(request.form.get('daily_mission_multiplier', 1.0))
            },
            'daily_events': {
                'enabled': request.form.get('daily_events_enabled') == 'on',
                'events': [
                    {
                        'id': 1,
                        'name': request.form.get('event1_name', '双倍经验'),
                        'start_time': request.form.get('event1_start', '10:00:00'),
                        'end_time': request.form.get('event1_end', '12:00:00')
                    },
                    {
                        'id': 2,
                        'name': request.form.get('event2_name', '金币翻倍'),
                        'start_time': request.form.get('event2_start', '18:00:00'),
                        'end_time': request.form.get('event2_end', '20:00:00')
                    }
                ]
            },
            'daily_limits': {
                'max_spins': int(request.form.get('max_spins', 1000)),
                'max_bet': int(request.form.get('max_bet', 1000000)),
                'max_win': int(request.form.get('max_win', 10000000))
            }
        }
        
        result = api.set_daily_config(config_data)
        
        if result.get('success'):
            flash('每日配置更新成功', 'success')
        else:
            flash(f'更新每日配置失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'更新每日配置失败: {str(e)}', 'error')
    
    return redirect(url_for('config.daily_config'))

@bp.route('/update')
@login_required
def update_config():
    """更新配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_update_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('config/update.html', config_data=config_data)
        else:
            flash(f'获取更新配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('config.config_management'))
    except Exception as e:
        flash(f'获取更新配置失败: {str(e)}', 'error')
        return redirect(url_for('config.config_management'))

@bp.route('/update/default')
@login_required
def update_default_config():
    """更新默认配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_update_default_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('config/update_default.html', config_data=config_data)
        else:
            flash(f'获取更新默认配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('config.config_management'))
    except Exception as e:
        flash(f'获取更新默认配置失败: {str(e)}', 'error')
        return redirect(url_for('config.config_management'))

@bp.route('/update', methods=['POST'])
@login_required
def save_update_config():
    """保存更新配置"""
    api = GameServerAPI()
    try:
        # 获取表单数据
        config_data = {
            'version_info': {
                'current_version': request.form.get('current_version', '1.0.0'),
                'latest_version': request.form.get('latest_version', '1.0.0'),
                'update_available': request.form.get('update_available') == 'on',
                'force_update': request.form.get('force_update') == 'on'
            },
            'update_settings': {
                'auto_update': request.form.get('auto_update') == 'on',
                'update_check_interval': int(request.form.get('check_interval', 1800)),
                'download_timeout': int(request.form.get('download_timeout', 600)),
                'retry_count': int(request.form.get('retry_count', 5))
            },
            'update_channels': {
                'stable': {
                    'enabled': request.form.get('stable_enabled') == 'on',
                    'url': request.form.get('stable_url', 'https://update.example.com/stable'),
                    'priority': int(request.form.get('stable_priority', 1))
                },
                'beta': {
                    'enabled': request.form.get('beta_enabled') == 'on',
                    'url': request.form.get('beta_url', 'https://update.example.com/beta'),
                    'priority': int(request.form.get('beta_priority', 2))
                },
                'alpha': {
                    'enabled': request.form.get('alpha_enabled') == 'on',
                    'url': request.form.get('alpha_url', 'https://update.example.com/alpha'),
                    'priority': int(request.form.get('alpha_priority', 3))
                }
            },
            'rollback_settings': {
                'enabled': request.form.get('rollback_enabled') == 'on',
                'keep_versions': int(request.form.get('keep_versions', 5)),
                'auto_rollback_on_error': request.form.get('auto_rollback') == 'on'
            }
        }
        
        result = api.set_update_config(config_data)
        
        if result.get('success'):
            flash('更新配置保存成功', 'success')
        else:
            flash(f'保存更新配置失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'保存更新配置失败: {str(e)}', 'error')
    
    return redirect(url_for('config.update_config'))