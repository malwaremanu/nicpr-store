from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .. import db
import json

bp = Blueprint('master', __name__)

schema = {
  "divisions": {
    "name": "divisions",
    "items": [
      {
        "name": "division_id",
        "type": "text",
        "label": "ID",
        "required": True
      },
      {
        "name": "division_name",
        "type": "text",
        "label": "Name",
        "required": True
      },
      {
        "name": "division_description",
        "type": "text",
        "label": "Description",
        "required": True
      },
      {
        "name": "division_head",
        "type": "select",
        "label": "Head",
        "required": True,
        "values" : [ str(a['name']) + ' (' + str(a['employee_id']) + ")"for a in db('users').fetch()]
      }      
    ]
  }    
}

@bp.route('/masters/<entity>', methods=['GET', 'POST'])
def crud(entity):    
    sc = schema[entity]
    if request.method == 'POST':
        data = request.json
        master_table = db(entity)
        master_table.put(data)
        print("done.", data)
        return jsonify({'message': 'Item added successfully'}), 201

    master_table = db(entity)
    all_items = master_table.fetchall()
    print(sc)
    return render_template('master.html', items=all_items, schema=sc)

@bp.route('/masters/<entity>/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def crud_item(entity, item_id):
    sc = schema[entity]
    master_table = db(entity)
    item = master_table.get(item_id)
    print(item)

    if request.method == 'PUT':
        data = request.json
        master_table.update(data, item_id)
        return jsonify({'message': 'Item updated successfully'}), 200

    if request.method == 'DELETE':
        master_table.delete(item_id)
        return jsonify({'message': 'Item deleted successfully'}), 200

    return render_template('master.html', item=item, schema=sc, item_id=item_id)