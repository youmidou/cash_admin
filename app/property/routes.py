from flask import render_template, flash, redirect, url_for, request, jsonify
from app.property import bp
from app.api_client import GameServerAPI
from app.auth import login_required
import json

@bp.route('/')
@login_required
def property_management():
    """属性管理主页面"""
    return render_template('property/management.html', title='属性管理')

@bp.route('/get', methods=['GET', 'POST'])
@login_required
def get_property():
    """获取属性值页面"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        uid = request.form.get('uid', type=int)
        key = request.form.get('key', '').strip()
        
        if not uid:
            flash('用户ID不能为空', 'error')
            return redirect(url_for('property.get_property'))
        
        if not key:
            flash('属性键不能为空', 'error')
            return redirect(url_for('property.get_property'))
        
        try:
            result = api.get_property_value(uid, key)
            
            if result.get('success'):
                property_data = result.get('data', {})
                flash(f'获取属性值成功: {key} = {property_data.get("value")}', 'success')
                return render_template('property/get_property.html', 
                                     title='获取属性值', 
                                     property_data=property_data,
                                     uid=uid,
                                     key=key)
            else:
                flash(f'获取属性值失败: {result.get("error", "未知错误")}', 'error')
                
        except Exception as e:
            flash(f'获取属性值失败: {str(e)}', 'error')
    
    return render_template('property/get_property.html', title='获取属性值')

@bp.route('/set', methods=['GET', 'POST'])
@login_required
def set_property():
    """设置属性值页面"""
    api = GameServerAPI()
    
    if request.method == 'POST':
        uid = request.form.get('uid', type=int)
        key = request.form.get('key', '').strip()
        value = request.form.get('value', '').strip()
        
        if not uid:
            flash('用户ID不能为空', 'error')
            return redirect(url_for('property.set_property'))
        
        if not key:
            flash('属性键不能为空', 'error')
            return redirect(url_for('property.set_property'))
        
        if not value:
            flash('属性值不能为空', 'error')
            return redirect(url_for('property.set_property'))
        
        try:
            # 尝试转换数据类型
            try:
                # 尝试转换为数字
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
                elif value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                elif value.startswith('{') or value.startswith('['):
                    # JSON格式
                    value = json.loads(value)
            except (ValueError, json.JSONDecodeError):
                # 保持字符串格式
                pass
            
            result = api.set_property_value(uid, key, value)
            
            if result.get('success'):
                flash(f'设置属性值成功: {key} = {value}', 'success')
                return redirect(url_for('property.get_property'))
            else:
                flash(f'设置属性值失败: {result.get("error", "未知错误")}', 'error')
                
        except Exception as e:
            flash(f'设置属性值失败: {str(e)}', 'error')
    
    return render_template('property/set_property.html', title='设置属性值')

@bp.route('/default')
@login_required
def property_default():
    """属性默认值页面"""
    api = GameServerAPI()
    try:
        result = api.get_property_default()
        
        if result.get('success'):
            default_data = result.get('data', {})
            return render_template('property/default.html', 
                                 title='属性默认值', 
                                 default_data=default_data)
        else:
            flash(f'获取属性默认值失败: {result.get("error", "未知错误")}', 'error')
            return redirect(url_for('property.property_management'))
    except Exception as e:
        flash(f'获取属性默认值失败: {str(e)}', 'error')
        return redirect(url_for('property.property_management'))

@bp.route('/set_default', methods=['POST'])
@login_required
def set_property_default():
    """设置属性为默认值"""
    api = GameServerAPI()
    try:
        uid = request.form.get('uid', type=int)
        key = request.form.get('key', '').strip()
        
        if not uid:
            flash('用户ID不能为空', 'error')
            return redirect(url_for('property.property_default'))
        
        if not key:
            flash('属性键不能为空', 'error')
            return redirect(url_for('property.property_default'))
        
        # 获取默认值
        default_result = api.get_property_default()
        
        if default_result.get('success'):
            default_data = default_result.get('data', {})
            
            # 查找默认值
            default_value = None
            for category, properties in default_data.items():
                if isinstance(properties, dict) and key in properties:
                    default_value = properties[key]
                    break
            
            if default_value is not None:
                # 设置属性为默认值
                result = api.set_property_value(uid, key, default_value)
                
                if result.get('success'):
                    flash(f'属性 {key} 已重置为默认值: {default_value}', 'success')
                else:
                    flash(f'重置属性失败: {result.get("error", "未知错误")}', 'error')
            else:
                flash(f'未找到属性 {key} 的默认值', 'error')
        else:
            flash(f'获取默认值失败: {default_result.get("error", "未知错误")}', 'error')
            
    except Exception as e:
        flash(f'重置属性失败: {str(e)}', 'error')
    
    return redirect(url_for('property.property_default'))
