from flask import render_template, flash, redirect, url_for, request, jsonify
from app.quest import bp
from app.api_client import GameServerAPI
from app.auth import login_required
import json

@bp.route('/')
@login_required
def quest_management():
    """任务管理主页面"""
    return render_template('quest/management.html', title='任务管理')

@bp.route('/info', methods=['GET', 'POST'])
@login_required
def quest_info():
    """获取任务信息页面"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        uid = request.form.get('uid', type=int)
        quest_id = request.form.get('quest_id', type=int)
        
        if not uid:
            flash('用户ID不能为空', 'error')
            return redirect(url_for('quest.quest_info'))
        
        try:
            result = api.get_quest_info(uid, quest_id)
            
            if result.get('success'):
                quest_data = result.get('data', {})
                flash(f'获取用户{uid}的任务信息成功', 'success')
                return render_template('quest/quest_info.html', 
                                     title='任务信息', 
                                     quest_data=quest_data,
                                     uid=uid,
                                     quest_id=quest_id)
            else:
                flash(f'获取任务信息失败: {result.get("error", "未知错误")}', 'error')
                
        except Exception as e:
            flash(f'获取任务信息失败: {str(e)}', 'error')
    
    return render_template('quest/quest_info.html', title='任务信息')

@bp.route('/rank')
@login_required
def quest_rank():
    """任务排行榜页面"""
    api = GameServerAPI()
    try:
        quest_type = request.args.get('quest_type', 'all')
        limit = request.args.get('limit', 50, type=int)
        
        result = api.get_quest_rank(quest_type, limit)
        
        if result.get('success'):
            rank_data = result.get('data', {})
            return render_template('quest/quest_rank.html', 
                                 title='任务排行榜', 
                                 rank_data=rank_data,
                                 quest_type=quest_type,
                                 limit=limit)
        else:
            flash(f'获取任务排行榜失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('quest.quest_management'))
    except Exception as e:
        flash(f'获取任务排行榜失败: {str(e)}', 'error')
        return redirect(url_for('quest.quest_management'))

@bp.route('/reset', methods=['GET', 'POST'])
@login_required
def reset_quest():
    """重置任务页面"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        uid = request.form.get('uid', type=int)
        quest_id = request.form.get('quest_id', type=int)
        quest_type = request.form.get('quest_type', 'all')
        
        if not uid:
            flash('用户ID不能为空', 'error')
            return redirect(url_for('quest.reset_quest'))
        
        try:
            result = api.reset_quest(uid, quest_id, quest_type)
            
            if result.get('success'):
                flash(f'重置用户{uid}的任务成功', 'success')
                return redirect(url_for('quest.quest_info'))
            else:
                flash(f'重置任务失败: {result.get("error", "未知错误")}', 'error')
                
        except Exception as e:
            flash(f'重置任务失败: {str(e)}', 'error')
    
    return render_template('quest/reset_quest.html', title='重置任务')

@bp.route('/clean', methods=['GET', 'POST'])
@login_required
def clean_quest_data():
    """清理任务数据页面"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        clean_type = request.form.get('clean_type', 'all')
        days_old = request.form.get('days_old', 30, type=int)
        
        try:
            result = api.clean_quest_data(clean_type, days_old)
            
            if result.get('success'):
                cleaned_records = result.get('data', {}).get('cleaned_records', 0)
                flash(f'任务数据清理成功，清理了{cleaned_records}条记录', 'success')
                return redirect(url_for('quest.quest_management'))
            else:
                flash(f'清理任务数据失败: {result.get("error", "未知错误")}', 'error')
                
        except Exception as e:
            flash(f'清理任务数据失败: {str(e)}', 'error')
    
    return render_template('quest/clean_quest_data.html', title='清理任务数据')

@bp.route('/default')
@login_required
def quest_default():
    """任务默认配置页面"""
    api = GameServerAPI()
    try:
        result = api.get_quest_default()
        
        if result.get('success'):
            default_data = result.get('data', {})
            return render_template('quest/default.html', 
                                 title='任务默认配置', 
                                 default_data=default_data)
        else:
            flash(f'获取任务默认配置失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('quest.quest_management'))
    except Exception as e:
        flash(f'获取任务默认配置失败: {str(e)}', 'error')
        return redirect(url_for('quest.quest_management'))

