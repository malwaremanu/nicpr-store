from flask import Blueprint, render_template, request, redirect, url_for
from .. import db

bp = Blueprint('inventory', __name__)

@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        store_id = request.form['store_id']
        description = request.form['description']
        date_of_procurement = request.form['date_of_procurement']
        warranty = request.form['warranty']
        expiry_date = request.form['expiry_date']
        bill_number = request.form['bill_number']
        category = request.form['category']

        inventory_table = db('inventory')
        new_inventory = {
            'store_id': store_id,
            'description': description,
            'date_of_procurement': date_of_procurement,
            'warranty': warranty,
            'expiry_date': expiry_date,
            'bill_number': bill_number,
            'category': category
        }
        inventory_table.put(new_inventory)
        return redirect(url_for('inventory'))
    return render_template('inventory_form.html')

@bp.route('/edit_inventory/<int:inventory_id>', methods=['GET', 'POST'])
def edit_inventory(inventory_id):
    inventory_table = db('inventory')
    inventory = inventory_table.get(inventory_id)
    if request.method == 'POST':
        inventory['store_id'] = request.form['store_id']
        inventory['description'] = request.form['description']
        inventory['date_of_procurement'] = request.form['date_of_procurement']
        inventory['warranty'] = request.form['warranty']
        inventory['expiry_date'] = request.form['expiry_date']
        inventory['bill_number'] = request.form['bill_number']
        inventory['category'] = request.form['category']
        inventory_table.update(inventory, inventory_id)
        return redirect(url_for('inventory'))
    return render_template('inventory_form.html', inventory=inventory)

@bp.route('/delete_inventory/<int:inventory_id>', methods=['POST'])
def delete_inventory(inventory_id):
    inventory_table = db('inventory')
    inventory_table.delete(inventory_id)
    return redirect(url_for('inventory'))