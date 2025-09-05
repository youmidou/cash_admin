from flask import render_template, request, jsonify, flash, redirect, url_for
from app.theme import bp
from app.api_client import GameServerAPI

@bp.route('/')
def theme_list():
    """主题列表页面"""
    api = GameServerAPI()
    themes_data = api.get_themes()
    
    return render_template('theme/list.html', themes_data=themes_data)

@bp.route('/<int:theme_id>')
def theme_detail(theme_id):
    """主题详情页面"""
    api = GameServerAPI()
    theme_info = api.get_theme(theme_id)
    
    if theme_info.get('error'):
        flash(f'获取主题信息失败: {theme_info["error"]}', 'error')
        return redirect(url_for('theme.theme_list'))
    
    return render_template('theme/detail.html', theme_info=theme_info)

@bp.route('/<int:theme_id>/config', methods=['GET', 'POST'])
def theme_config(theme_id):
    """主题配置页面"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        # 收集配置数据
        config_data = {}
        
        # 基础配置
        if request.form.get('active'):
            config_data['active'] = request.form.get('active') == 'on'
        if request.form.get('min_bet'):
            config_data['min_bet'] = int(request.form.get('min_bet'))
        if request.form.get('max_bet'):
            config_data['max_bet'] = int(request.form.get('max_bet'))
        if request.form.get('rtp'):
            config_data['rtp'] = float(request.form.get('rtp'))
        
        # 特殊功能配置
        if request.form.get('has_bonus'):
            config_data['has_bonus'] = request.form.get('has_bonus') == 'on'
        if request.form.get('has_free_spins'):
            config_data['has_free_spins'] = request.form.get('has_free_spins') == 'on'
        if request.form.get('has_jackpot'):
            config_data['has_jackpot'] = request.form.get('has_jackpot') == 'on'
        
        result = api.set_theme_config(theme_id, config_data)
        
        if result.get('error'):
            flash(f'更新主题配置失败: {result["error"]}', 'error')
        else:
            flash('主题配置更新成功', 'success')
            return redirect(url_for('theme.theme_detail', theme_id=theme_id))
    
    # GET 请求，获取主题和配置信息
    theme_info = api.get_theme(theme_id)
    config_info = api.get_theme_config(theme_id)
    
    if theme_info.get('error'):
        flash(f'获取主题信息失败: {theme_info["error"]}', 'error')
        return redirect(url_for('theme.theme_list'))
    
    return render_template('theme/config.html', 
                         theme_info=theme_info, 
                         config_info=config_info)

@bp.route('/<int:theme_id>/users')
def theme_users(theme_id):
    """主题用户统计页面"""
    api = GameServerAPI()
    theme_info = api.get_theme(theme_id)
    
    if theme_info.get('error'):
        flash(f'获取主题信息失败: {theme_info["error"]}', 'error')
        return redirect(url_for('theme.theme_list'))
    
    # 这里可以添加获取主题用户统计的API调用
    users_data = {'users': [], 'total': 0}  # 占位数据
    
    return render_template('theme/users.html', 
                         theme_info=theme_info, 
                         users_data=users_data)
