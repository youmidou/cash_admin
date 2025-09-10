from functools import wraps
from flask import session, redirect, url_for, request, flash
import requests
import json

def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('请先登录管理员账户', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def verify_admin_credentials(username, password):
    """验证管理员凭据"""
    # 这里应该连接到游戏服务器验证管理员身份
    # 暂时使用简单的硬编码验证
    admin_users = {
        'admin': 'admin123',
        'root': 'root123',
        'manager': 'manager123'
    }
    
    return admin_users.get(username) == password

def get_admin_info(username):
    """获取管理员信息"""
    admin_info = {
        'username': username,
        'role': 'admin',
        'permissions': ['user_management', 'theme_management', 'config_management', 'activity_management']
    }
    return admin_info
