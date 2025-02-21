from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .. import db
from datetime import datetime

bp = Blueprint('indent', __name__)

@bp.route('/create_indent', methods=['GET', 'POST'])
def create_indent():
    indents = db('indents')
    if request.method == 'POST':
        # indent_number = '123' nomenclature to be decided
        indentor_id = session['user']['name']
        items = request.form['items']
        # quantity = request.form['quantity']
        # remarks = request.form['remarks']
        # priority = request.form['priority']
        
        new_indent = {
            'description': description,
            'indentor_id': indentor_id,
            'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'Pending',
            'priority': priority,
            'remarks': remarks
        }
        indents.put(new_indent)
        flash('Indent created successfully', 'success')
        return redirect(url_for('indent.view_indents'))
    return render_template('indent_form.html',indents=indents.fetchall())

@bp.route('/view_indents', methods=['GET'])
def view_indents():
    indents_table = db('indents')
    all_indents = indents_table.fetchall()
    return render_template('view_indents.html', indents=all_indents)

@bp.route('/approve_indent/<indent_id>', methods=['POST'])
def approve_indent(indent_id):
    indents_table = db('indents')
    indent = indents_table.get(indent_id)
    if indent:
        indent['status'] = 'Approved'
        indent['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        indents_table.update(indent, indent_id)
        flash('Indent approved successfully', 'success')
    return redirect(url_for('indent.view_indents'))

@bp.route('/reject_indent/<indent_id>', methods=['POST'])
def reject_indent(indent_id):
    indents_table = db('indents')
    indent = indents_table.get(indent_id)
    if indent:
        indent['status'] = 'Rejected'
        indent['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        indents_table.update(indent, indent_id)
        flash('Indent rejected successfully', 'success')
    return redirect(url_for('indent.view_indents'))

@bp.route('/fulfill_indent/<indent_id>', methods=['POST'])
def fulfill_indent(indent_id):
    indents_table = db('indents')
    indent = indents_table.get(indent_id)
    if indent:
        indent['status'] = 'Fulfilled'
        indent['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        indents_table.update(indent, indent_id)
        flash('Indent fulfilled successfully', 'success')
    return redirect(url_for('indent.view_indents'))

@bp.route('/add_indent_item/<indent_id>', methods=['GET', 'POST'])
def add_indent_item(indent_id):
    store_master_table = db('store_master')
    inventory_table = db('inventory')
    store_master = store_master_table.fetchall()
    inventory = inventory_table.fetchall()

    if request.method == 'POST':
        required_item = request.form['required_item']
        quantity = request.form['quantity']
        issued_item = request.form['issued_item']

        indent_items_table = db('indent_items')
        new_indent_item = {
            'indent_id': indent_id,
            'required_item': required_item,
            'quantity': quantity,
            'status': 'Pending',
            'action_by': session['user_id'],
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'issued_item': issued_item
        }
        indent_items_table.put(new_indent_item)
        flash('Indent item added successfully', 'success')
        return redirect(url_for('indent.view_indents'))
    return render_template('add_indent_item.html', indent_id=indent_id, store_master=store_master, inventory=inventory)