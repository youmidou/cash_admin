from flask import render_template, request, jsonify, flash, redirect, url_for
from app.main import bp
from app.api_client import GameServerAPI

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    """仪表板页面"""
    api = GameServerAPI()
    
    # 获取系统信息
    system_info = api.get_system_info()
    
    # 获取用户统计
    users_data = api.get_users(page=1, limit=10)
    
    # 获取主题列表
    themes_data = api.get_themes()
    
    return render_template('dashboard.html', 
                         system_info=system_info,
                         users_data=users_data,
                         themes_data=themes_data)

@bp.route('/api/stats')
def api_stats():
    """获取统计数据的 API"""
    api = GameServerAPI()
    
    try:
        # 获取各种统计数据
        system_info = api.get_system_info()
        users_data = api.get_users(page=1, limit=100)
        
        stats = {
            'total_users': users_data.get('total', 0) if users_data.get('error') is None else 0,
            'online_users': system_info.get('online_users', 0) if system_info.get('error') is None else 0,
            'server_status': 'online' if system_info.get('error') is None else 'offline',
            'system_info': system_info
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
