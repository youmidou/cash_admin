from flask import render_template, request, jsonify, flash, redirect, url_for
from app.jackpot import bp
from app.api_client import GameServerAPI
from app.auth import login_required

@bp.route('/')
@login_required
def jackpot_management():
    """奖池管理主页面"""
    return render_template('jackpot/management.html')

@bp.route('/info/<int:theme_id>')
@login_required
def jackpot_info(theme_id):
    """获取指定主题的奖池信息"""
    api = GameServerAPI()
    try:
        result = api.get_jackpot_info(theme_id)
        if result.get('success'):
            jackpot_data = result.get('data', {})
            return render_template('jackpot/info.html', jackpot=jackpot_data, theme_id=theme_id)
        else:
            flash(f'获取奖池信息失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('jackpot.jackpot_management'))
    except Exception as e:
        flash(f'获取奖池信息失败: {str(e)}', 'error')
        return redirect(url_for('jackpot.jackpot_management'))

@bp.route('/all')
@login_required
def all_jackpot_info():
    """获取所有奖池信息"""
    api = GameServerAPI()
    try:
        result = api.get_all_jackpot_info()
        if result.get('success'):
            data = result.get('data', {})
            jackpots = data.get('jackpots', [])
            total_contribution = data.get('total_contribution', 0)
            total_themes = data.get('total_themes', 0)
            return render_template('jackpot/all_info.html', 
                                 jackpots=jackpots, 
                                 total_contribution=total_contribution,
                                 total_themes=total_themes)
        else:
            flash(f'获取所有奖池信息失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('jackpot.jackpot_management'))
    except Exception as e:
        flash(f'获取所有奖池信息失败: {str(e)}', 'error')
        return redirect(url_for('jackpot.jackpot_management'))

@bp.route('/calculate-store', methods=['GET', 'POST'])
@login_required
def calculate_store_data():
    """计算商店数据"""
    if request.method == 'POST':
        api = GameServerAPI()
        try:
            theme_id = request.form.get('theme_id')
            if theme_id:
                theme_id = int(theme_id)
            calculation_type = request.form.get('calculation_type', 'all')
            date_range = request.form.get('date_range', 'today')
            
            result = api.calculate_store_data(theme_id, calculation_type, date_range)
            
            if result.get('success'):
                store_data = result.get('data', {})
                return render_template('jackpot/store_calculation.html', 
                                     store_data=store_data,
                                     theme_id=theme_id,
                                     calculation_type=calculation_type,
                                     date_range=date_range)
            else:
                flash(f'计算商店数据失败: {result.get("error", "未知错误")}', 'error')
        except Exception as e:
            flash(f'计算商店数据失败: {str(e)}', 'error')
    
    return render_template('jackpot/calculate_store.html')

