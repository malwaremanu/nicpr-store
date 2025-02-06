from flask import Blueprint, render_template, request, redirect, url_for, session
from .. import db

bp = Blueprint('indent', __name__)

@bp.route('/create_indent', methods=['GET', 'POST'])
def create_indent():
    if request.method == 'POST':
        description = request.form['description']
        indentor_id = session['user_id']
        indents = db('indents')
        new_indent = {
            'description': description,
            'indentor_id': indentor_id,
            'status': 'Pending'
        }
        indents.put(new_indent)
        return redirect(url_for('dashboard'))
    return render_template('indent_form.html')

@bp.route('/approve_indent/<int:indent_id>', methods=['POST'])
def approve_indent(indent_id):
    indents = db('indents')
    indent = indents.get(indent_id)
    if indent:
        indent['status'] = 'Approved'
        indents.update(indent, indent_id)
    return redirect(url_for('dashboard'))

@bp.route('/reject_indent/<int:indent_id>', methods=['POST'])
def reject_indent(indent_id):
    indents = db('indents')
    indent = indents.get(indent_id)
    if indent:
        indent['status'] = 'Rejected'
        indents.update(indent, indent_id)
    return redirect(url_for('dashboard'))