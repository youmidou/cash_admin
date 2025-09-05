from flask import render_template, request, jsonify, flash, redirect, url_for
from app.main import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
def index():
    """首页重定向到登录或仪表板"""
    from flask import session
    if 'admin_logged_in' in session:
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
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
@login_required
def api_stats():
    """获取统计数据的 API"""
    api = GameServerAPI()
    
    try:
        # 获取在线用户数量
        online_data = api.get_online_users()
        online_count = online_data.get('online_user_num', 0) if online_data.get('error') is None else 0
        
        # 获取系统信息
        system_info = api.get_system_info()
        
        # 获取用户映射信息
        user_map_data = api.get_user_map()
        
        stats = {
            'total_users': user_map_data.get('total', 5) if user_map_data.get('error') is None else 5,
            'online_users': online_count,
            'server_status': 'online' if online_data.get('error') is None else 'offline',
            'system_info': system_info,
            'user_map': user_map_data
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
