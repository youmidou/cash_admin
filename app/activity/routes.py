from flask import render_template, request, jsonify, flash, redirect, url_for
from app.activity import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
@login_required
def activity_management():
    """活动管理主页面"""
    return render_template('activity/management.html')

@bp.route('/config')
@login_required
def activity_config():
    """活动配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_activity_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('activity/config.html', config_data=config_data)
        else:
            flash(f'获取活动配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('activity.activity_management'))
    except Exception as e:
        flash(f'获取活动配置失败: {str(e)}', 'error')
        return redirect(url_for('activity.activity_management'))

@bp.route('/config', methods=['POST'])
@login_required
def update_activity_config():
    """更新活动配置"""
    api = GameServerAPI()
    try:
        # 获取表单数据
        config_data = {
            'login_bonus': {
                'enabled': request.form.get('login_bonus_enabled') == 'on',
                'daily_bonus': {
                    'base_coins': int(request.form.get('daily_bonus_base_coins', 0)),
                    'multiplier': float(request.form.get('daily_bonus_multiplier', 1.0)),
                    'max_days': int(request.form.get('daily_bonus_max_days', 7))
                },
                'weekly_bonus': {
                    'base_coins': int(request.form.get('weekly_bonus_base_coins', 0)),
                    'multiplier': float(request.form.get('weekly_bonus_multiplier', 1.0)),
                    'reset_day': int(request.form.get('weekly_bonus_reset_day', 1))
                },
                'monthly_bonus': {
                    'base_coins': int(request.form.get('monthly_bonus_base_coins', 0)),
                    'multiplier': float(request.form.get('monthly_bonus_multiplier', 1.0)),
                    'reset_day': int(request.form.get('monthly_bonus_reset_day', 1))
                }
            },
            'daily_mission': {
                'enabled': request.form.get('daily_mission_enabled') == 'on',
                'missions': [
                    {
                        'id': 1,
                        'name': request.form.get('mission1_name', '每日登录'),
                        'type': request.form.get('mission1_type', 'login'),
                        'target': int(request.form.get('mission1_target', 1)),
                        'reward': {'coins': int(request.form.get('mission1_reward', 0))},
                        'enabled': request.form.get('mission1_enabled') == 'on'
                    },
                    {
                        'id': 2,
                        'name': request.form.get('mission2_name', '旋转10次'),
                        'type': request.form.get('mission2_type', 'spin'),
                        'target': int(request.form.get('mission2_target', 10)),
                        'reward': {'coins': int(request.form.get('mission2_reward', 0))},
                        'enabled': request.form.get('mission2_enabled') == 'on'
                    },
                    {
                        'id': 3,
                        'name': request.form.get('mission3_name', '获胜5次'),
                        'type': request.form.get('mission3_type', 'win'),
                        'target': int(request.form.get('mission3_target', 5)),
                        'reward': {'coins': int(request.form.get('mission3_reward', 0))},
                        'enabled': request.form.get('mission3_enabled') == 'on'
                    }
                ],
                'reset_time': request.form.get('mission_reset_time', '00:00:00')
            },
            'special_events': {
                'enabled': request.form.get('special_events_enabled') == 'on',
                'events': [
                    {
                        'id': 1,
                        'name': request.form.get('event1_name', '双倍经验日'),
                        'type': request.form.get('event1_type', 'double_exp'),
                        'start_time': request.form.get('event1_start_time', ''),
                        'end_time': request.form.get('event1_end_time', ''),
                        'enabled': request.form.get('event1_enabled') == 'on'
                    },
                    {
                        'id': 2,
                        'name': request.form.get('event2_name', '金币翻倍'),
                        'type': request.form.get('event2_type', 'double_coins'),
                        'start_time': request.form.get('event2_start_time', ''),
                        'end_time': request.form.get('event2_end_time', ''),
                        'enabled': request.form.get('event2_enabled') == 'on'
                    }
                ]
            }
        }
        
        result = api.set_activity_config(config_data)
        
        if result.get('success'):
            flash('活动配置更新成功', 'success')
        else:
            flash(f'更新活动配置失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'更新活动配置失败: {str(e)}', 'error')
    
    return redirect(url_for('activity.activity_config'))

@bp.route('/config/default')
@login_required
def activity_default_config():
    """活动默认配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_activity_default_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('activity/config_default.html', config_data=config_data)
        else:
            flash(f'获取活动默认配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('activity.activity_management'))
    except Exception as e:
        flash(f'获取活动默认配置失败: {str(e)}', 'error')
        return redirect(url_for('activity.activity_management'))

@bp.route('/ac')
@login_required
def ac_management():
    """AC管理主页面"""
    return render_template('activity/ac_management.html')

@bp.route('/ac/config')
@login_required
def ac_config():
    """AC配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_ac_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('activity/ac_config.html', config_data=config_data)
        else:
            flash(f'获取AC配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('activity.ac_management'))
    except Exception as e:
        flash(f'获取AC配置失败: {str(e)}', 'error')
        return redirect(url_for('activity.ac_management'))

@bp.route('/ac/config', methods=['POST'])
@login_required
def update_ac_config():
    """更新AC配置"""
    api = GameServerAPI()
    try:
        # 获取表单数据
        config_data = {
            'achievement_system': {
                'enabled': request.form.get('achievement_enabled') == 'on',
                'categories': [
                    {
                        'id': 1,
                        'name': request.form.get('category1_name', '登录成就'),
                        'achievements': [
                            {
                                'id': 1,
                                'name': request.form.get('achievement1_name', '首次登录'),
                                'description': request.form.get('achievement1_desc', '完成首次登录'),
                                'target': int(request.form.get('achievement1_target', 1)),
                                'reward': {'coins': int(request.form.get('achievement1_reward', 0))},
                                'enabled': request.form.get('achievement1_enabled') == 'on'
                            },
                            {
                                'id': 2,
                                'name': request.form.get('achievement2_name', '连续登录7天'),
                                'description': request.form.get('achievement2_desc', '连续登录7天'),
                                'target': int(request.form.get('achievement2_target', 7)),
                                'reward': {'coins': int(request.form.get('achievement2_reward', 0))},
                                'enabled': request.form.get('achievement2_enabled') == 'on'
                            }
                        ]
                    },
                    {
                        'id': 2,
                        'name': request.form.get('category2_name', '游戏成就'),
                        'achievements': [
                            {
                                'id': 3,
                                'name': request.form.get('achievement3_name', '旋转100次'),
                                'description': request.form.get('achievement3_desc', '累计旋转100次'),
                                'target': int(request.form.get('achievement3_target', 100)),
                                'reward': {'coins': int(request.form.get('achievement3_reward', 0))},
                                'enabled': request.form.get('achievement3_enabled') == 'on'
                            },
                            {
                                'id': 4,
                                'name': request.form.get('achievement4_name', '获胜50次'),
                                'description': request.form.get('achievement4_desc', '累计获胜50次'),
                                'target': int(request.form.get('achievement4_target', 50)),
                                'reward': {'coins': int(request.form.get('achievement4_reward', 0))},
                                'enabled': request.form.get('achievement4_enabled') == 'on'
                            }
                        ]
                    }
                ]
            },
            'collection_system': {
                'enabled': request.form.get('collection_enabled') == 'on',
                'collections': [
                    {
                        'id': 1,
                        'name': request.form.get('collection1_name', '金币收集'),
                        'description': request.form.get('collection1_desc', '收集指定数量的金币'),
                        'target': int(request.form.get('collection1_target', 0)),
                        'reward': {'gems': int(request.form.get('collection1_reward', 0))},
                        'enabled': request.form.get('collection1_enabled') == 'on'
                    },
                    {
                        'id': 2,
                        'name': request.form.get('collection2_name', '宝石收集'),
                        'description': request.form.get('collection2_desc', '收集指定数量的宝石'),
                        'target': int(request.form.get('collection2_target', 0)),
                        'reward': {'coins': int(request.form.get('collection2_reward', 0))},
                        'enabled': request.form.get('collection2_enabled') == 'on'
                    }
                ]
            }
        }
        
        result = api.set_ac_config(config_data)
        
        if result.get('success'):
            flash('AC配置更新成功', 'success')
        else:
            flash(f'更新AC配置失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'更新AC配置失败: {str(e)}', 'error')
    
    return redirect(url_for('activity.ac_config'))

@bp.route('/ac/config/default')
@login_required
def ac_default_config():
    """AC默认配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_ac_default_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('activity/ac_config_default.html', config_data=config_data)
        else:
            flash(f'获取AC默认配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('activity.ac_management'))
    except Exception as e:
        flash(f'获取AC默认配置失败: {str(e)}', 'error')
        return redirect(url_for('activity.ac_management'))

