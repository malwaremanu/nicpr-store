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
  },

  "store_items": {
    "name": "store items",
    "items": [
      {
        "name": "item_id",
        "type": "text",
        "label": "Store Item ID",
        "required": True
      },
      {
        "name": "item_name",
        "type": "text",
        "label": "Item Name",
        "required": True
      },
      {
        "name": "item_description",
        "type": "text",
        "label": "Item Description",
        "required": True
      },
      {
        "name": "item_type",
        "type": "select",
        "label": "Item Type",
        "required": True,
        "values" : ['Stock','Non_Stock']
      },
      {
        "name": "buffer_quantity",
        "type": "text",
        "label": "Buffer Quantity",
        "required": True
      }    
    ]
  },

  "inventory": {
    "name": "inventory",
    "items": [
      {
        "name": "item_id",
        "type": "select",
        "label": "Store Item ID/Name",
        "required": True,
        "values" : [ str(a['item_id']) + '-' + str(a['item_name']) for a in db('store_items').fetch()]
      },
      {
        "name": "serial_number",
        "type": "text",
        "label": "Serial Number/Batch Number",
        "required": True
      },
      {
        "name": "category",
        "type": "select",
        "label": "Item Category",
        "required": True,
        "values" : ['Equipment/Asset','Consumable','Stationary','Gift']
      },
      {
        "name": "item_description",
        "type": "text",
        "label": "Item Description",
        "required": True
      },
      {
        "name": "quantity",
        "type": "number",
        "label": "Quantity",
        "required": True
      },
      {
        "name": "receipt_date",
        "type": "date",
        "label": "Date of Receipt",
        "required": True
      },
      {
        "name": "bill_number",
        "type": "text",
        "label": "Bill Number",
        "required": True
      }   
    ]
  },

  "indents": {
    "name": "indents",
    "items": [
      {
        "name": "item_id",
        "type": "select",
        "label": "Store Item ID/Name",
        "required": True,
        "values" : [ str(a['item_id']) + '-' + str(a['item_name']) for a in db('store_items').fetch()]
      },
      {
        "name": "quantity",
        "type": "number",
        "label": "Required Quantity",
        "required": True
      },
      {
        "name": "remarks",
        "type": "text",
        "label": "Remarks",
        "required": True
      }
    ]
  }  
    
}

@bp.route('/masters/<entity>', methods=['GET','PUT'])
def crud(entity):    
    sc = schema[entity]
    if request.method == 'PUT':
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