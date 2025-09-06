from flask import render_template, request, jsonify, flash, redirect, url_for
from app.cheat import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
@login_required
def cheat_management():
    """作弊管理主页面"""
    return render_template('cheat/management.html')

@bp.route('/execute', methods=['GET', 'POST'])
@login_required
def execute_cheat():
    """执行作弊操作页面"""
    if request.method == 'POST':
        api = GameServerAPI()
        try:
            user_id = int(request.form.get('user_id'))
            cheat_type = request.form.get('cheat_type')
            reason = request.form.get('reason', '管理员调试')
            
            # 构建作弊参数
            cheat_params = {}
            if request.form.get('cheat_coins'):
                cheat_params['coins'] = int(request.form.get('cheat_coins'))
            if request.form.get('cheat_gems'):
                cheat_params['gems'] = int(request.form.get('cheat_gems'))
            if request.form.get('cheat_level'):
                cheat_params['level'] = int(request.form.get('cheat_level'))
            if request.form.get('cheat_vip'):
                cheat_params['vip_level'] = int(request.form.get('cheat_vip'))
            if request.form.get('cheat_theme'):
                cheat_params['theme_id'] = int(request.form.get('cheat_theme'))
            if request.form.get('cheat_bet'):
                cheat_params['bet_amount'] = int(request.form.get('cheat_bet'))
            
            result = api.execute_cheat(user_id, cheat_type, cheat_params, reason)
            
            if result.get('success'):
                flash('作弊操作执行成功', 'success')
                return redirect(url_for('cheat.cheat_management'))
            else:
                flash(f'作弊操作执行失败: {result.get("error", "未知错误")}', 'error')
        except Exception as e:
            flash(f'作弊操作执行失败: {str(e)}', 'error')
    
    return render_template('cheat/execute_cheat.html')

@bp.route('/respin', methods=['GET', 'POST'])
@login_required
def respin_cheat():
    """重新旋转作弊页面"""
    if request.method == 'POST':
        api = GameServerAPI()
        try:
            user_id = int(request.form.get('user_id'))
            theme_id = int(request.form.get('theme_id', 10050))
            bet_amount = int(request.form.get('bet_amount', 1000))
            reason = request.form.get('reason', '管理员调试')
            
            # 构建目标结果
            target_result = {}
            if request.form.get('target_win'):
                target_result['win_amount'] = int(request.form.get('target_win'))
            if request.form.get('target_jackpot'):
                target_result['jackpot'] = request.form.get('target_jackpot') == 'on'
            if request.form.get('target_bonus'):
                target_result['bonus'] = request.form.get('target_bonus') == 'on'
            if request.form.get('target_free_spins'):
                target_result['free_spins'] = int(request.form.get('target_free_spins', 0))
            
            result = api.respin_cheat(user_id, theme_id, bet_amount, target_result, reason)
            
            if result.get('success'):
                flash('重新旋转作弊执行成功', 'success')
                return redirect(url_for('cheat.cheat_management'))
            else:
                flash(f'重新旋转作弊执行失败: {result.get("error", "未知错误")}', 'error')
        except Exception as e:
            flash(f'重新旋转作弊执行失败: {str(e)}', 'error')
    
    return render_template('cheat/respin_cheat.html')

@bp.route('/clean-disconnect-data', methods=['GET', 'POST'])
@login_required
def clean_disconnect_data():
    """清理断开连接数据页面"""
    if request.method == 'POST':
        api = GameServerAPI()
        try:
            user_id = request.form.get('user_id')
            if user_id:
                user_id = int(user_id)
            clean_type = request.form.get('clean_type', 'all')
            reason = request.form.get('reason', '管理员清理')
            
            result = api.clean_disconnect_data(user_id, clean_type, reason)
            
            if result.get('success'):
                flash('断开连接数据清理成功', 'success')
                return redirect(url_for('cheat.cheat_management'))
            else:
                flash(f'断开连接数据清理失败: {result.get("error", "未知错误")}', 'error')
        except Exception as e:
            flash(f'断开连接数据清理失败: {str(e)}', 'error')
    
    return render_template('cheat/clean_disconnect_data.html')
