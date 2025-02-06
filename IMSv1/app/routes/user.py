from flask import Blueprint, render_template, request, redirect, url_for, flash
from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

bp = Blueprint('user', __name__)

@bp.route('/', methods=['GET'])
def index():
    users_table = db('users')
    indents_table = db('indents')
    store_master_table = db('store_master')
    inventory_table = db('inventory')

    total_users = users_table.count()
    total_indents = indents_table.count()
    total_store_masters = store_master_table.count()
    total_inventory_items = inventory_table.count()

    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    return render_template('dashboard.html', total_users=total_users, total_indents=total_indents, total_store_masters=total_store_masters, total_inventory_items=total_inventory_items, greeting=greeting)

@bp.route('/users', methods=['GET', 'POST'])
def users():    
    users_table = db('users')
    all_users = users_table.fetchall()
    return render_template('user_form.html', users=all_users)

@bp.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    users_table = db('users')
    user = users_table.get(user_id)
    if request.method == 'POST':
        user['employee_id'] = request.form['employee_id']
        user['name'] = request.form['name']
        user['designation'] = request.form['designation']
        user['division_id'] = request.form['division_id']
        user['mobile_no'] = request.form['mobile_no']
        user['email'] = request.form['email']
        user['role'] = request.form['role']
        user['status'] = request.form['status']
        users_table.update(user, user_id)
        flash('User updated successfully', 'success')
        return redirect(url_for('user.users'))
    return render_template('user_form.html', user=user, user_id=user_id)

@bp.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    users_table = db('users')
    users_table.delete(user_id)
    flash('User deleted successfully', 'success')
    return redirect(url_for('user.users'))

@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    users_table = db('users')
    all_users = users_table.fetchall()
    if request.method == 'POST':
        user_id = request.form['user_id']
        new_password = request.form['new_password']
        user = users_table.get(user_id)
        if user:
            print("user found ->", user)
            user['password'] = new_password
            users_table.update(user, user_id)
            flash('Password changed successfully', 'success')
        else:
            flash('User not found', 'error')
        return redirect(url_for('user.change_password'))
    return render_template('change_password.html', users=all_users)

@bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        designation = request.form['designation']
        division_id = request.form['division_id']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        role = request.form['role']
        status = request.form['status']
        password = request.form['password']
        permissions = request.form['permissions']

        users_table = db('users')
        new_user = {
            'employee_id': employee_id,
            'name': name,
            'designation': designation,
            'division_id': division_id,
            'mobile_no': mobile_no,
            'email': email,
            'role': role,
            'permissions' : permissions,
            'status': status,
            'password': password
        }
        users_table.put(new_user)
        flash('User created successfully', 'success')
        return redirect(url_for('user.users'))
    return render_template('user_form.html')