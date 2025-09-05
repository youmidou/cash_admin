from flask import render_template, request, jsonify, flash, redirect, url_for
from app.user import bp
from app.api_client import GameServerAPI

@bp.route('/')
def user_list():
    """用户列表页面"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    api = GameServerAPI()
    users_data = api.get_users(page=page, limit=50, search=search)
    
    return render_template('user/list.html', 
                         users_data=users_data,
                         current_page=page,
                         search=search)

@bp.route('/<int:user_id>')
def user_detail(user_id):
    """用户详情页面"""
    api = GameServerAPI()
    user_info = api.get_user_info(user_id)
    
    if user_info.get('error'):
        flash(f'获取用户信息失败: {user_info["error"]}', 'error')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/detail.html', user_info=user_info)

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def user_edit(user_id):
    """编辑用户信息"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        updates = {}
        
        # 收集表单数据
        if request.form.get('level'):
            updates['level'] = int(request.form.get('level'))
        if request.form.get('vip_level'):
            updates['vip_level'] = int(request.form.get('vip_level'))
        if request.form.get('coins'):
            updates['coins'] = int(request.form.get('coins'))
        if request.form.get('gems'):
            updates['gems'] = int(request.form.get('gems'))
        
        result = api.update_user(user_id, updates)
        
        if result.get('error'):
            flash(f'更新用户失败: {result["error"]}', 'error')
        else:
            flash('用户信息更新成功', 'success')
            return redirect(url_for('user.user_detail', user_id=user_id))
    
    # GET 请求，获取用户信息
    user_info = api.get_user_info(user_id)
    
    if user_info.get('error'):
        flash(f'获取用户信息失败: {user_info["error"]}', 'error')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/edit.html', user_info=user_info)

@bp.route('/<int:user_id>/delete', methods=['POST'])
def user_delete(user_id):
    """删除用户账户"""
    api = GameServerAPI()
    result = api.delete_account(user_id)
    
    if result.get('error'):
        flash(f'删除用户失败: {result["error"]}', 'error')
    else:
        flash('用户账户删除成功', 'success')
    
    return redirect(url_for('user.user_list'))

@bp.route('/<int:user_id>/send-prize', methods=['GET', 'POST'])
def send_prize(user_id):
    """发送奖励给用户"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        prize_data = {
            'type': request.form.get('prize_type'),
            'amount': int(request.form.get('amount', 0)),
            'message': request.form.get('message', '')
        }
        
        result = api.send_prize(user_id, prize_data)
        
        if result.get('error'):
            flash(f'发送奖励失败: {result["error"]}', 'error')
        else:
            flash('奖励发送成功', 'success')
            return redirect(url_for('user.user_detail', user_id=user_id))
    
    # GET 请求，获取用户信息
    user_info = api.get_user_info(user_id)
    
    if user_info.get('error'):
        flash(f'获取用户信息失败: {user_info["error"]}', 'error')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/send_prize.html', user_info=user_info)

@bp.route('/<int:user_id>/cheat', methods=['GET', 'POST'])
def user_cheat(user_id):
    """用户作弊功能"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        cheat_type = request.form.get('cheat_type')
        value = request.form.get('value')
        
        result = api.cheat(user_id, cheat_type, value)
        
        if result.get('error'):
            flash(f'执行作弊失败: {result["error"]}', 'error')
        else:
            flash('作弊执行成功', 'success')
            return redirect(url_for('user.user_detail', user_id=user_id))
    
    # GET 请求，获取用户信息
    user_info = api.get_user_info(user_id)
    
    if user_info.get('error'):
        flash(f'获取用户信息失败: {user_info["error"]}', 'error')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/cheat.html', user_info=user_info)
