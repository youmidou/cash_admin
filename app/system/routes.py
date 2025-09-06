from flask import render_template, request, flash, redirect, url_for, jsonify
from app.system import bp
from app.api_client import GameServerAPI
from app.auth import login_required
import json

@bp.route('/')
@login_required
def system_management():
    """系统管理页面"""
    api = GameServerAPI()
    
    # 获取系统信息
    system_info = api.get_system_info()
    
    return render_template('system/management.html', 
                         system_info=system_info)

@bp.route('/update-config', methods=['POST'])
@login_required
def update_config():
    """更新系统配置"""
    api = GameServerAPI()
    
    try:
        # 获取表单数据
        config_data = {}
        for key, value in request.form.items():
            if key.startswith('config_'):
                config_key = key.replace('config_', '')
                config_data[config_key] = value
        
        # 调用API更新配置
        result = api.update_system_config(config_data)
        
        if result.get('success'):
            flash('系统配置更新成功', 'success')
        else:
            flash(f'系统配置更新失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'系统配置更新失败: {str(e)}', 'error')
    
    return redirect(url_for('system.system_management'))

@bp.route('/set-today-begin', methods=['POST'])
@login_required
def set_today_begin():
    """设置今日开始时间"""
    api = GameServerAPI()
    
    try:
        begin_time = request.form.get('begin_time')
        if not begin_time:
            flash('请选择开始时间', 'error')
            return redirect(url_for('system.system_management'))
        
        # 调用API设置今日开始时间
        result = api.set_today_begin(begin_time)
        
        if result.get('success'):
            flash(f'今日开始时间已设置为: {begin_time}', 'success')
        else:
            flash(f'设置今日开始时间失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'设置今日开始时间失败: {str(e)}', 'error')
    
    return redirect(url_for('system.system_management'))

@bp.route('/reset-time', methods=['POST'])
@login_required
def reset_time():
    """重置系统时间"""
    api = GameServerAPI()
    
    try:
        reset_type = request.form.get('reset_type', 'all')
        
        # 调用API重置系统时间
        result = api.reset_system_time(reset_type)
        
        if result.get('success'):
            flash(f'系统时间重置成功: {reset_type}', 'success')
        else:
            flash(f'重置系统时间失败: {result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'重置系统时间失败: {str(e)}', 'error')
    
    return redirect(url_for('system.system_management'))

# API路由
@bp.route('/api/system-info')
@login_required
def api_system_info():
    """获取系统信息的API"""
    api = GameServerAPI()
    
    try:
        system_info = api.get_system_info()
        return jsonify(system_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
