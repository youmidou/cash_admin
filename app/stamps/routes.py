from flask import render_template, request, jsonify, flash, redirect, url_for
from app.stamps import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
@login_required
def stamps_management():
    """邮票管理主页面"""
    return render_template('stamps/management.html')

@bp.route('/config')
@login_required
def stamps_config():
    """邮票配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_stamps_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('stamps/config.html', config_data=config_data)
        else:
            flash(f'获取邮票配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('stamps.stamps_management'))
    except Exception as e:
        flash(f'获取邮票配置失败: {str(e)}', 'error')
        return redirect(url_for('stamps.stamps_management'))

@bp.route('/config', methods=['POST'])
@login_required
def update_stamps_config():
    """更新邮票配置"""
    api = GameServerAPI()
    try:
        # 获取表单数据
        config_data = {
            'stamp_system': {
                'enabled': request.form.get('stamp_system_enabled') == 'on',
                'max_stamps_per_user': int(request.form.get('max_stamps_per_user', 1000)),
                'stamp_expire_days': int(request.form.get('stamp_expire_days', 30)),
                'auto_cleanup_enabled': request.form.get('auto_cleanup_enabled') == 'on',
                'cleanup_interval_hours': int(request.form.get('cleanup_interval_hours', 24))
            },
            'stamp_types': [
                {
                    'id': 1,
                    'name': request.form.get('stamp_type_1_name', '普通邮票'),
                    'type': 'normal',
                    'rarity': 'common',
                    'value': int(request.form.get('stamp_type_1_value', 1)),
                    'description': request.form.get('stamp_type_1_description', '基础邮票，用于日常收集'),
                    'icon': 'stamp_normal',
                    'color': request.form.get('stamp_type_1_color', '#4CAF50'),
                    'enabled': request.form.get('stamp_type_1_enabled') == 'on'
                },
                {
                    'id': 2,
                    'name': request.form.get('stamp_type_2_name', '稀有邮票'),
                    'type': 'rare',
                    'rarity': 'rare',
                    'value': int(request.form.get('stamp_type_2_value', 5)),
                    'description': request.form.get('stamp_type_2_description', '稀有邮票，价值较高'),
                    'icon': 'stamp_rare',
                    'color': request.form.get('stamp_type_2_color', '#2196F3'),
                    'enabled': request.form.get('stamp_type_2_enabled') == 'on'
                },
                {
                    'id': 3,
                    'name': request.form.get('stamp_type_3_name', '史诗邮票'),
                    'type': 'epic',
                    'rarity': 'epic',
                    'value': int(request.form.get('stamp_type_3_value', 15)),
                    'description': request.form.get('stamp_type_3_description', '史诗邮票，非常珍贵'),
                    'icon': 'stamp_epic',
                    'color': request.form.get('stamp_type_3_color', '#9C27B0'),
                    'enabled': request.form.get('stamp_type_3_enabled') == 'on'
                },
                {
                    'id': 4,
                    'name': request.form.get('stamp_type_4_name', '传说邮票'),
                    'type': 'legendary',
                    'rarity': 'legendary',
                    'value': int(request.form.get('stamp_type_4_value', 50)),
                    'description': request.form.get('stamp_type_4_description', '传说邮票，极其稀有'),
                    'icon': 'stamp_legendary',
                    'color': request.form.get('stamp_type_4_color', '#FF9800'),
                    'enabled': request.form.get('stamp_type_4_enabled') == 'on'
                }
            ],
            'stamp_rewards': {
                'daily_login': {
                    'enabled': request.form.get('daily_login_enabled') == 'on',
                    'stamps': [
                        {'type_id': 1, 'count': int(request.form.get('daily_login_type_1_count', 1)), 'probability': float(request.form.get('daily_login_type_1_prob', 0.6))},
                        {'type_id': 2, 'count': int(request.form.get('daily_login_type_2_count', 1)), 'probability': float(request.form.get('daily_login_type_2_prob', 0.3))},
                        {'type_id': 3, 'count': int(request.form.get('daily_login_type_3_count', 1)), 'probability': float(request.form.get('daily_login_type_3_prob', 0.1))}
                    ]
                },
                'game_play': {
                    'enabled': request.form.get('game_play_enabled') == 'on',
                    'stamps_per_spin': float(request.form.get('stamps_per_spin', 0.1)),
                    'bonus_multiplier': float(request.form.get('bonus_multiplier', 2.0)),
                    'max_stamps_per_day': int(request.form.get('max_stamps_per_day', 50))
                },
                'purchase': {
                    'enabled': request.form.get('purchase_enabled') == 'on',
                    'stamps_per_dollar': int(request.form.get('stamps_per_dollar', 10)),
                    'bonus_stamps': int(request.form.get('bonus_stamps', 5))
                }
            },
            'stamp_exchange': {
                'enabled': request.form.get('exchange_enabled') == 'on',
                'exchange_rates': [
                    {'from_type': 1, 'to_type': 2, 'rate': int(request.form.get('exchange_rate_1_to_2', 5))},
                    {'from_type': 2, 'to_type': 3, 'rate': int(request.form.get('exchange_rate_2_to_3', 3))},
                    {'from_type': 3, 'to_type': 4, 'rate': int(request.form.get('exchange_rate_3_to_4', 3))}
                ],
                'exchange_fee_percent': int(request.form.get('exchange_fee_percent', 10))
            }
        }
        
        result = api.set_stamps_config(config_data)
        
        if result.get('success'):
            flash('邮票配置更新成功', 'success')
        else:
            flash(f'更新邮票配置失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'更新邮票配置失败: {str(e)}', 'error')
    
    return redirect(url_for('stamps.stamps_config'))

@bp.route('/config/default')
@login_required
def stamps_default_config():
    """邮票默认配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_stamps_default_config()
        
        if result.get('success'):
            default_config = result.get('data', {})
            return render_template('stamps/default_config.html', default_config=default_config)
        else:
            flash(f'获取邮票默认配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('stamps.stamps_management'))
    except Exception as e:
        flash(f'获取邮票默认配置失败: {str(e)}', 'error')
        return redirect(url_for('stamps.stamps_management'))

@bp.route('/config/reset', methods=['POST'])
@login_required
def reset_stamps_config():
    """重置邮票配置为默认值"""
    api = GameServerAPI()
    try:
        # 获取默认配置
        default_result = api.get_stamps_default_config()
        
        if default_result.get('success'):
            default_config = default_result.get('data', {})
            
            # 设置配置为默认值
            result = api.set_stamps_config(default_config)
            
            if result.get('success'):
                flash('邮票配置已重置为默认值', 'success')
            else:
                flash(f'重置邮票配置失败: {result.get("error", "未知错误")}', 'error')
        else:
            flash(f'获取默认配置失败: {default_result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'重置邮票配置失败: {str(e)}', 'error')
    
    return redirect(url_for('stamps.stamps_config'))
