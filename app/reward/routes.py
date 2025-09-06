from flask import render_template, request, jsonify, flash, redirect, url_for
from app.reward import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
@login_required
def reward_management():
    """奖励管理主页面"""
    return render_template('reward/management.html')

@bp.route('/send-prize', methods=['GET', 'POST'])
@login_required
def send_prize():
    """发送奖励页面"""
    if request.method == 'POST':
        api = GameServerAPI()
        try:
            user_id = int(request.form.get('user_id'))
            prize_type = request.form.get('prize_type')
            amount = int(request.form.get('amount', 0))
            reason = request.form.get('reason', '管理员奖励')
            
            result = api.send_prize(user_id, prize_type, amount, reason)
            
            if result.get('success'):
                flash('奖励发送成功', 'success')
                return redirect(url_for('reward.reward_management'))
            else:
                flash(f'奖励发送失败: {result.get("error", "未知错误")}', 'error')
        except Exception as e:
            flash(f'奖励发送失败: {str(e)}', 'error')
    
    return render_template('reward/send_prize.html')

@bp.route('/add-inbox', methods=['GET', 'POST'])
@login_required
def add_inbox():
    """添加收件箱物品页面"""
    if request.method == 'POST':
        api = GameServerAPI()
        try:
            user_id = int(request.form.get('user_id'))
            item_type = request.form.get('item_type')
            item_id = request.form.get('item_id')
            quantity = int(request.form.get('quantity', 1))
            title = request.form.get('title', '管理员礼物')
            description = request.form.get('description', '')
            
            result = api.add_inbox(user_id, item_type, item_id, quantity, title, description)
            
            if result.get('success'):
                flash('收件箱物品添加成功', 'success')
                return redirect(url_for('reward.reward_management'))
            else:
                flash(f'收件箱物品添加失败: {result.get("error", "未知错误")}', 'error')
        except Exception as e:
            flash(f'收件箱物品添加失败: {str(e)}', 'error')
    
    return render_template('reward/add_inbox.html')

@bp.route('/delete-inbox-gift', methods=['GET', 'POST'])
@login_required
def delete_inbox_gift():
    """删除收件箱礼物页面"""
    if request.method == 'POST':
        api = GameServerAPI()
        try:
            user_id = int(request.form.get('user_id'))
            gift_id = request.form.get('gift_id')
            
            result = api.delete_inbox_gift(user_id, gift_id)
            
            if result.get('success'):
                flash('收件箱礼物删除成功', 'success')
                return redirect(url_for('reward.reward_management'))
            else:
                flash(f'收件箱礼物删除失败: {result.get("error", "未知错误")}', 'error')
        except Exception as e:
            flash(f'收件箱礼物删除失败: {str(e)}', 'error')
    
    return render_template('reward/delete_inbox_gift.html')

@bp.route('/send-inbox-gift', methods=['GET', 'POST'])
@login_required
def send_inbox_gift():
    """发送收件箱礼物页面"""
    if request.method == 'POST':
        api = GameServerAPI()
        try:
            user_id = int(request.form.get('user_id'))
            gift_type = request.form.get('gift_type')
            sender_name = request.form.get('sender_name', '管理员')
            message = request.form.get('message', '')
            
            # 构建礼物数据
            gift_data = {}
            if request.form.get('gift_coins'):
                gift_data['coins'] = int(request.form.get('gift_coins'))
            if request.form.get('gift_gems'):
                gift_data['gems'] = int(request.form.get('gift_gems'))
            if request.form.get('gift_items'):
                gift_data['items'] = request.form.get('gift_items')
            
            result = api.send_inbox_gift(user_id, gift_type, gift_data, sender_name, message)
            
            if result.get('success'):
                flash('收件箱礼物发送成功', 'success')
                return redirect(url_for('reward.reward_management'))
            else:
                flash(f'收件箱礼物发送失败: {result.get("error", "未知错误")}', 'error')
        except Exception as e:
            flash(f'收件箱礼物发送失败: {str(e)}', 'error')
    
    return render_template('reward/send_inbox_gift.html')

