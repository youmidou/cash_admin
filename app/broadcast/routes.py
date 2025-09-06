from flask import render_template, request, jsonify, flash, redirect, url_for
from app.broadcast import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
@login_required
def broadcast_management():
    """广播管理主页面"""
    return render_template('broadcast/management.html')

@bp.route('/config')
@login_required
def broadcast_config():
    """广播配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_broadcast_config()
        
        if result.get('success'):
            config_data = result.get('data', {})
            return render_template('broadcast/config.html', config_data=config_data)
        else:
            flash(f'获取广播配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('broadcast.broadcast_management'))
    except Exception as e:
        flash(f'获取广播配置失败: {str(e)}', 'error')
        return redirect(url_for('broadcast.broadcast_management'))

@bp.route('/config', methods=['POST'])
@login_required
def update_broadcast_config():
    """更新广播配置"""
    api = GameServerAPI()
    try:
        # 获取表单数据
        config_data = {
            'system_broadcast': {
                'enabled': request.form.get('system_broadcast_enabled') == 'on',
                'max_length': int(request.form.get('system_broadcast_max_length', 200)),
                'cooldown_seconds': int(request.form.get('system_broadcast_cooldown', 30)),
                'auto_delete_after': int(request.form.get('system_broadcast_auto_delete', 3600)),
                'allowed_types': request.form.getlist('system_broadcast_types'),
                'default_type': request.form.get('system_broadcast_default_type', 'info')
            },
            'user_broadcast': {
                'enabled': request.form.get('user_broadcast_enabled') == 'on',
                'max_length': int(request.form.get('user_broadcast_max_length', 100)),
                'cooldown_seconds': int(request.form.get('user_broadcast_cooldown', 60)),
                'auto_delete_after': int(request.form.get('user_broadcast_auto_delete', 1800)),
                'allowed_types': request.form.getlist('user_broadcast_types'),
                'default_type': request.form.get('user_broadcast_default_type', 'info'),
                'min_level_required': int(request.form.get('user_broadcast_min_level', 5)),
                'cost_coins': int(request.form.get('user_broadcast_cost', 1000))
            },
            'admin_broadcast': {
                'enabled': request.form.get('admin_broadcast_enabled') == 'on',
                'max_length': int(request.form.get('admin_broadcast_max_length', 500)),
                'cooldown_seconds': int(request.form.get('admin_broadcast_cooldown', 10)),
                'auto_delete_after': int(request.form.get('admin_broadcast_auto_delete', 7200)),
                'allowed_types': request.form.getlist('admin_broadcast_types'),
                'default_type': request.form.get('admin_broadcast_default_type', 'announcement'),
                'require_admin_key': request.form.get('admin_broadcast_require_key') == 'on'
            },
            'broadcast_channels': {
                'global': {
                    'enabled': request.form.get('channel_global_enabled') == 'on',
                    'name': request.form.get('channel_global_name', '全服广播'),
                    'description': request.form.get('channel_global_description', '发送给所有在线玩家的广播')
                },
                'level_based': {
                    'enabled': request.form.get('channel_level_enabled') == 'on',
                    'name': request.form.get('channel_level_name', '等级广播'),
                    'description': request.form.get('channel_level_description', '根据玩家等级发送的广播')
                },
                'vip_only': {
                    'enabled': request.form.get('channel_vip_enabled') == 'on',
                    'name': request.form.get('channel_vip_name', 'VIP广播'),
                    'description': request.form.get('channel_vip_description', '仅发送给VIP玩家的广播')
                },
                'region_based': {
                    'enabled': request.form.get('channel_region_enabled') == 'on',
                    'name': request.form.get('channel_region_name', '地区广播'),
                    'description': request.form.get('channel_region_description', '根据地区发送的广播')
                }
            }
        }
        
        result = api.set_broadcast_config(config_data)
        
        if result.get('success'):
            flash('广播配置更新成功', 'success')
        else:
            flash(f'更新广播配置失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'更新广播配置失败: {str(e)}', 'error')
    
    return redirect(url_for('broadcast.broadcast_config'))

@bp.route('/send')
@login_required
def send_broadcast():
    """发送广播页面"""
    api = GameServerAPI()
    try:
        # 获取广播配置和模板
        config_result = api.get_broadcast_config()
        if config_result.get('success'):
            config_data = config_result.get('data', {})
        else:
            config_data = {}
        
        return render_template('broadcast/send.html', config_data=config_data)
    except Exception as e:
        flash(f'获取广播配置失败: {str(e)}', 'error')
        return redirect(url_for('broadcast.broadcast_management'))

@bp.route('/send', methods=['POST'])
@login_required
def send_broadcast_message():
    """发送广播消息"""
    api = GameServerAPI()
    try:
        # 获取表单数据
        broadcast_data = {
            'message': request.form.get('message', '').strip(),
            'type': request.form.get('type', 'info'),
            'channel': request.form.get('channel', 'global'),
            'target_users': request.form.get('target_users', 'all'),
            'expires_at': request.form.get('expires_at'),
            'priority': request.form.get('priority', 'normal'),
            'template_id': request.form.get('template_id')
        }
        
        # 验证消息内容
        if not broadcast_data['message']:
            flash('广播消息内容不能为空', 'error')
            return redirect(url_for('broadcast.send_broadcast'))
        
        result = api.send_broadcast(broadcast_data)
        
        if result.get('success'):
            flash('广播消息发送成功', 'success')
            return redirect(url_for('broadcast.broadcast_history'))
        else:
            flash(f'发送广播消息失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'发送广播消息失败: {str(e)}', 'error')
    
    return redirect(url_for('broadcast.send_broadcast'))

@bp.route('/history')
@login_required
def broadcast_history():
    """广播历史记录页面"""
    api = GameServerAPI()
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        result = api.get_broadcast_history(page, limit)
        
        if result.get('success'):
            history_data = result.get('data', {})
            return render_template('broadcast/history.html', 
                                 history_data=history_data, 
                                 current_page=page,
                                 limit=limit)
        else:
            flash(f'获取广播历史记录失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('broadcast.broadcast_management'))
    except Exception as e:
        flash(f'获取广播历史记录失败: {str(e)}', 'error')
        return redirect(url_for('broadcast.broadcast_management'))

@bp.route('/sender-key')
@login_required
def broadcast_sender_key():
    """广播发送者密钥页面"""
    api = GameServerAPI()
    try:
        result = api.get_broadcast_sender_key()
        
        if result.get('success'):
            key_data = result.get('data', {})
            return render_template('broadcast/sender_key.html', key_data=key_data)
        else:
            flash(f'获取广播发送者密钥失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('broadcast.broadcast_management'))
    except Exception as e:
        flash(f'获取广播发送者密钥失败: {str(e)}', 'error')
        return redirect(url_for('broadcast.broadcast_management'))

