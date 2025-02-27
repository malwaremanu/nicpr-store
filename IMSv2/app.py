from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import os
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_development')

# Mock database (in a real app, use SQLAlchemy or similar)
# Load user data from JSON
USERS_FILE = 'users.json'

def get_users():
    if not os.path.exists(USERS_FILE):
        # Create default users if file doesn't exist
        default_users = {
            "1": {"id": "1", "username": "admin", "password": "1234", "role": "superadmin", "division_id": None},
            "2": {"id": "2", "username": "store_manager", "password": "1234", "role": "admin", "division_id": None},
            "3": {"id": "3", "username": "div_head", "password": "1234", "role": "division_head", "division_id": "1"},
            "4": {"id": "4", "username": "store_incharge", "password": "1234", "role": "store_incharge", "division_id": None},
            "5": {"id": "5", "username": "assistant", "password": "1234", "role": "store_assistant", "division_id": None},
            "6": {"id": "6", "username": "user1", "password": "1234", "role": "user", "division_id": "1"}
        }
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users
    
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Initialize data storage
# In production, use a proper database
ITEMS_FILE = 'items.json'
INVENTORY_FILE = 'inventory.json'
REQUESTS_FILE = 'requests.json'
DIVISIONS_FILE = 'divisions.json'

def get_items():
    if not os.path.exists(ITEMS_FILE):
        default_items = {
            "1": {"id": "1", "name": "Laptop", "description": "Standard office laptop", "category": "Electronics", "min_stock": 5, "unit_price": 800.00},
            "2": {"id": "2", "name": "Mouse", "description": "Wireless mouse", "category": "Electronics", "min_stock": 10, "unit_price": 25.00},
            "3": {"id": "3", "name": "Keyboard", "description": "Standard keyboard", "category": "Electronics", "min_stock": 10, "unit_price": 30.00},
            "4": {"id": "4", "name": "Notebook", "description": "A4 notebook", "category": "Stationery", "min_stock": 50, "unit_price": 3.50},
            "5": {"id": "5", "name": "Pen", "description": "Ballpoint pen", "category": "Stationery", "min_stock": 100, "unit_price": 1.00}
        }
        with open(ITEMS_FILE, 'w') as f:
            json.dump(default_items, f, indent=4)
        return default_items
    
    with open(ITEMS_FILE, 'r') as f:
        return json.load(f)

def get_inventory():
    if not os.path.exists(INVENTORY_FILE):
        default_inventory = {
            "1": {"id": "1", "item_id": "1", "quantity": 8, "location": "Main Store"},
            "2": {"id": "2", "item_id": "2", "quantity": 15, "location": "Main Store"},
            "3": {"id": "3", "item_id": "3", "quantity": 12, "location": "Main Store"},
            "4": {"id": "4", "item_id": "4", "quantity": 60, "location": "Main Store"},
            "5": {"id": "5", "item_id": "5", "quantity": 200, "location": "Main Store"}
        }
        with open(INVENTORY_FILE, 'w') as f:
            json.dump(default_inventory, f, indent=4)
        return default_inventory
    
    with open(INVENTORY_FILE, 'r') as f:
        return json.load(f)

def get_requests():
    if not os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, 'w') as f:
            json.dump({}, f, indent=4)
        return {}
    
    with open(REQUESTS_FILE, 'r') as f:
        return json.load(f)

def get_divisions():
    if not os.path.exists(DIVISIONS_FILE):
        default_divisions = {
            "1": {"id": "1", "name": "IT Department", "head_id": "3"},
            "2": {"id": "2", "name": "Finance Department", "head_id": None},
            "3": {"id": "3", "name": "HR Department", "head_id": None}
        }
        with open(DIVISIONS_FILE, 'w') as f:
            json.dump(default_divisions, f, indent=4)
        return default_divisions
    
    with open(DIVISIONS_FILE, 'r') as f:
        return json.load(f)

def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Middleware to check if user is logged in
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        users = get_users()
        g.user = users.get(str(user_id))

# Decorators for authentication and authorization
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Please log in to access this page.')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user is None:
                flash('Please log in to access this page.')
                return redirect(url_for('login', next=request.url))
            
            if g.user['role'] not in roles:
                flash('You do not have permission to access this page.')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def index():
    return render_template('base.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = get_users()
        user = next((user for user in users.values() if user['username'] == username), None)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            flash('You have successfully logged in!')
            
            # Redirect based on role
            if user['role'] in ['superadmin', 'admin']:
                return redirect(url_for('admin_dashboard'))
            elif user['role'] in ['division_head', 'store_incharge', 'store_assistant']:
                return redirect(url_for('request_list'))
            else:
                return redirect(url_for('index'))
        
        flash('Invalid username or password.')
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

# Admin routes
@app.route('/admin')
@role_required(['superadmin', 'admin'])
def admin_dashboard():
    items = get_items()
    inventory = get_inventory()
    requests = get_requests()
    
    # Count items by category
    categories = {}
    for item in items.values():
        cat = item['category']
        if cat in categories:
            categories[cat] += 1
        else:
            categories[cat] = 1
    
    # Get low stock items
    low_stock = []
    for inv in inventory.values():
        item = items.get(inv['item_id'])
        if item and inv['quantity'] < item['min_stock']:
            low_stock.append({
                'id': item['id'],
                'name': item['name'],
                'current': inv['quantity'],
                'min': item['min_stock']
            })
    
    # Count requests by status
    request_stats = {
        'pending': 0,
        'approved': 0,
        'fulfilled': 0,
        'rejected': 0
    }
    
    for req in requests.values():
        status = req.get('status', 'pending')
        if status in request_stats:
            request_stats[status] += 1
    
    return render_template(
        'admin/dashboard.html',
        item_count=len(items),
        categories=categories,
        low_stock=low_stock,
        request_stats=request_stats
    )

@app.route('/admin/items')
@role_required(['superadmin', 'admin'])
def admin_items():
    items = get_items()
    inventory = get_inventory()
    
    # Combine item and inventory data
    item_data = []
    for item_id, item in items.items():
        inv = next((inv for inv in inventory.values() if inv['item_id'] == item_id), None)
        quantity = inv['quantity'] if inv else 0
        
        item_data.append({
            'id': item_id,
            'name': item['name'],
            'description': item['description'],
            'category': item['category'],
            'min_stock': item['min_stock'],
            'current_stock': quantity,
            'unit_price': item['unit_price']
        })
    
    return render_template('admin/items.html', items=item_data)

@app.route('/admin/items/add', methods=['GET', 'POST'])
@role_required(['superadmin', 'admin'])
def admin_add_item():
    if request.method == 'POST':
        items = get_items()
        inventory = get_inventory()
        
        # Generate new IDs
        new_item_id = str(max(int(id) for id in items.keys()) + 1) if items else "1"
        new_inv_id = str(max(int(id) for id in inventory.keys()) + 1) if inventory else "1"
        
        # Create new item
        items[new_item_id] = {
            'id': new_item_id,
            'name': request.form['name'],
            'description': request.form['description'],
            'category': request.form['category'],
            'min_stock': int(request.form['min_stock']),
            'unit_price': float(request.form['unit_price'])
        }
        
        # Create inventory entry
        inventory[new_inv_id] = {
            'id': new_inv_id,
            'item_id': new_item_id,
            'quantity': int(request.form['initial_quantity']),
            'location': request.form['location']
        }
        
        save_data(items, ITEMS_FILE)
        save_data(inventory, INVENTORY_FILE)
        
        flash('Item added successfully.')
        return redirect(url_for('admin_items'))
    
    return render_template('admin/item_form.html', item=None)

@app.route('/admin/items/edit/<id>', methods=['GET', 'POST'])
@role_required(['superadmin', 'admin'])
def admin_edit_item(id):
    items = get_items()
    inventory = get_inventory()
    
    item = items.get(id)
    if not item:
        flash('Item not found.')
        return redirect(url_for('admin_items'))
    
    inv = next((inv for inv in inventory.values() if inv['item_id'] == id), None)
    
    if request.method == 'POST':
        # Update item
        item['name'] = request.form['name']
        item['description'] = request.form['description']
        item['category'] = request.form['category']
        item['min_stock'] = int(request.form['min_stock'])
        item['unit_price'] = float(request.form['unit_price'])
        
        # Update inventory
        if inv:
            inv['quantity'] = int(request.form['quantity'])
            inv['location'] = request.form['location']
        
        save_data(items, ITEMS_FILE)
        save_data(inventory, INVENTORY_FILE)
        
        flash('Item updated successfully.')
        return redirect(url_for('admin_items'))
    
    # Prepare data for template
    item_data = {
        'id': id,
        'name': item['name'],
        'description': item['description'],
        'category': item['category'],
        'min_stock': item['min_stock'],
        'unit_price': item['unit_price'],
        'quantity': inv['quantity'] if inv else 0,
        'location': inv['location'] if inv else ''
    }
    
    return render_template('admin/item_form.html', item=item_data)

@app.route('/admin/users')
@role_required(['superadmin'])
def admin_users():
    users = get_users()
    divisions = get_divisions()
    
    user_data = []
    for user in users.values():
        division = divisions.get(user['division_id']) if user['division_id'] else None
        
        user_data.append({
            'id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'division': division['name'] if division else 'N/A'
        })
    
    return render_template('admin/users.html', users=user_data)

# Inventory routes
@app.route('/inventory')
@login_required
def inventory_list():
    items = get_items()
    inventory = get_inventory()
    
    # Combine item and inventory data
    inventory_data = []
    for inv_id, inv in inventory.items():
        item = items.get(inv['item_id'])
        if item:
            is_low = inv['quantity'] < item['min_stock']
            
            inventory_data.append({
                'id': inv_id,
                'item_id': inv['item_id'],
                'name': item['name'],
                'category': item['category'],
                'quantity': inv['quantity'],
                'min_stock': item['min_stock'],
                'location': inv['location'],
                'is_low': is_low
            })
    
    return render_template('inventory/list.html', inventory=inventory_data)

@app.route('/inventory/<id>')
@login_required
def inventory_detail(id):
    items = get_items()
    inventory = get_inventory()
    
    inv = inventory.get(id)
    if not inv:
        flash('Inventory item not found.')
        return redirect(url_for('inventory_list'))
    
    item = items.get(inv['item_id'])
    if not item:
        flash('Associated item not found.')
        return redirect(url_for('inventory_list'))
    
    # Get request history for this item
    requests = get_requests()
    request_history = []
    
    for req_id, req in requests.items():
        for req_item in req.get('items', []):
            if req_item['item_id'] == inv['item_id']:
                request_history.append({
                    'id': req_id,
                    'date': req['date'],
                    'requester': req['requester_name'],
                    'quantity': req_item['quantity'],
                    'status': req['status']
                })
    
    # Sort by date, most recent first
    request_history.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template(
        'inventory/detail.html',
        item=item,
        inventory=inv,
        request_history=request_history
    )

# Request routes
@app.route('/request/new', methods=['GET', 'POST'])
@login_required
def request_new():
    if request.method == 'POST':
        users = get_users()
        items = get_items()
        requests = get_requests()
        
        # Generate new request ID
        new_id = str(max(int(id) for id in requests.keys()) + 1) if requests else "1"
        
        # Get requested items
        requested_items = []
        for key, value in request.form.items():
            if key.startswith('item_') and value and int(value) > 0:
                item_id = key.split('_')[1]
                requested_items.append({
                    'item_id': item_id,
                    'quantity': int(value),
                    'fulfilled': 0,
                    'status': 'pending'
                })
        
        if not requested_items:
            flash('Please select at least one item.')
            return redirect(url_for('request_new'))
        
        # Create new request
        import datetime
        
        requests[new_id] = {
            'id': new_id,
            'requester_id': g.user['id'],
            'requester_name': g.user['username'],
            'division_id': g.user['division_id'],
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'pending',
            'items': requested_items,
            'remarks': request.form['remarks'],
            'current_approver': 'division_head'  # First approver in workflow
        }
        
        save_data(requests, REQUESTS_FILE)
        
        flash('Request submitted successfully.')
        return redirect(url_for('request_list'))
    
    # Get available items for request form
    items = get_items()
    inventory = get_inventory()
    
    available_items = []
    for item_id, item in items.items():
        inv = next((inv for inv in inventory.values() if inv['item_id'] == item_id), None)
        quantity = inv['quantity'] if inv else 0
        
        if quantity > 0:
            available_items.append({
                'id': item_id,
                'name': item['name'],
                'description': item['description'],
                'category': item['category'],
                'available': quantity
            })
    
    return render_template('request/new.html', items=available_items)

@app.route('/request/list')
@login_required
def request_list():
    requests = get_requests()
    user_role = g.user['role']
    user_id = g.user['id']
    division_id = g.user['division_id']
    
    filtered_requests = []
    
    for req_id, req in requests.items():
        # Filter based on role
        if user_role == 'user':
            # Users see only their own requests
            if req['requester_id'] == user_id:
                filtered_requests.append(req)
        
        elif user_role == 'division_head':
            # Division heads see requests from their division
            if req['division_id'] == division_id:
                filtered_requests.append(req)
        
        elif user_role == 'store_incharge':
            # Store incharge sees requests approved by division head
            if req['current_approver'] == 'store_incharge' or req['current_approver'] in ['store_assistant', 'fulfilled']:
                filtered_requests.append(req)
        
        elif user_role == 'store_assistant':
            # Store assistant sees requests approved by store incharge
            if req['current_approver'] == 'store_assistant' or req['current_approver'] == 'fulfilled':
                filtered_requests.append(req)
        
        elif user_role in ['admin', 'superadmin']:
            # Admins see all requests
            filtered_requests.append(req)
    
    # Sort by date (most recent first)
    filtered_requests.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('request/list.html', requests=filtered_requests, user_role=user_role)

@app.route('/request/detail/<id>')
@login_required
def request_detail(id):
    requests = get_requests()
    items = get_items()
    
    req = requests.get(id)
    if not req:
        flash('Request not found.')
        return redirect(url_for('request_list'))
    
    # Resolve item details
    request_items = []
    for req_item in req['items']:
        item = items.get(req_item['item_id'])
        if item:
            request_items.append({
                'id': req_item['item_id'],
                'name': item['name'],
                'quantity': req_item['quantity'],
                'fulfilled': req_item['fulfilled'],
                'status': req_item['status']
            })
    
    return render_template(
        'request/detail.html',
        request=req,
        items=request_items,
        user_role=g.user['role']
    )

@app.route('/request/approve/<id>', methods=['GET', 'POST'])
@login_required
def request_approve(id):
    requests = get_requests()
    user_role = g.user['role']
    
    req = requests.get(id)
    if not req:
        flash('Request not found.')
        return redirect(url_for('request_list'))
    
    print(req)
    items = get_items()
    # Resolve item details
    request_items = []
    for req_item in req['items']:
        item = items.get(req_item['item_id'])
        if item:
            request_items.append({
                'id': req_item['item_id'],
                'name': item['name'],
                'quantity': req_item['quantity'],
                'fulfilled': req_item['fulfilled'],
                'status': req_item['status']
            })

    # Check authorization based on current approver
    if req['current_approver'] == 'division_head' and user_role != 'division_head':
        flash('You are not authorized to approve this request.')
        return redirect(url_for('request_detail', id=id))
    
    if req['current_approver'] == 'store_incharge' and user_role != 'store_incharge':
        flash('You are not authorized to approve this request.')
        return redirect(url_for('request_detail', id=id))
    
    if request.method == 'POST':
        action = request.form['action']
        
        if action == 'approve':
            # Update approver based on workflow
            if req['current_approver'] == 'division_head':
                req['current_approver'] = 'store_incharge'
                flash('Request approved and forwarded to Store Incharge.')
            
            elif req['current_approver'] == 'store_incharge':
                req['current_approver'] = 'store_assistant'
                flash('Request approved and forwarded to Store Assistant.')
            
            req['remarks'] += f"\n[{g.user['username']}]: Approved"
        
        elif action == 'reject':
            req['status'] = 'rejected'
            req['current_approver'] = 'rejected'
            req['remarks'] += f"\n[{g.user['username']}]: Rejected - {request.form['reject_reason']}"
            flash('Request has been rejected.')
        
        save_data(requests, REQUESTS_FILE)
        return redirect(url_for('request_list'))
    
    return render_template('request/approval.html', reqst=req, items=request_items,)

@app.route('/request/fulfill/<id>', methods=['GET', 'POST'])
@role_required(['store_assistant'])
def request_fulfill(id):
    requests = get_requests()
    items = get_items()
    inventory = get_inventory()
    
    req = requests.get(id)
    if not req:
        flash('Request not found.')
        return redirect(url_for('request_list'))
    
    # Check if this request is ready for fulfillment
    if req['current_approver'] != 'store_assistant':
        flash('This request is not ready for fulfillment.')
        return redirect(url_for('request_detail', id=id))
    
    if request.method == 'POST':
        purchase_items = []
        all_fulfilled = True
        
        # Process each requested item
        for req_item in req['items']:
            item_id = req_item['item_id']
            form_key = f"fulfill_{item_id}"
            
            if form_key in request.form:
                fulfill_qty = int(request.form[form_key])
                
                # Find inventory for this item
                inv = next((inv for inv in inventory.values() if inv['item_id'] == item_id), None)
                
                if inv and fulfill_qty > 0:
                    # Check if we have enough
                    if fulfill_qty > inv['quantity']:
                        fulfill_qty = inv['quantity']
                    
                    # Update inventory
                    inv['quantity'] -= fulfill_qty
                    
                    # Update request item
                    req_item['fulfilled'] = fulfill_qty
                    
                    if fulfill_qty < req_item['quantity']:
                        req_item['status'] = 'partially_fulfilled'
                        all_fulfilled = False
                        
                        # Add to purchase request if needed
                        remaining = req_item['quantity'] - fulfill_qty
                        purchase_items.append({
                            'item_id': item_id,
                            'name': items[item_id]['name'],
                            'quantity': remaining
                        })
                    else:
                        req_item['status'] = 'fulfilled'
        
        # Update request status
        if all_fulfilled:
            req['status'] = 'fulfilled'
            req['current_approver'] = 'fulfilled'
            flash('Request has been completely fulfilled.')
        else:
            req['status'] = 'partially_fulfilled'
            req['current_approver'] = 'fulfilled'
            flash('Request has been partially fulfilled. A purchase request will be created for the remaining items.')
        
        req['remarks'] += f"\n[{g.user['username']}]: Fulfilled items"
        
        save_data(requests, REQUESTS_FILE)
        save_data(inventory, INVENTORY_FILE)
        
        # Create purchase request if needed
        if purchase_items:
            session['purchase_items'] = purchase_items
            return redirect(url_for('request_purchase', request_id=id))
        
        return redirect(url_for('request_list'))
    
    # Prepare item data for the fulfillment form
    fulfillment_items = []
    for req_item in req['items']:
        item_id = req_item['item_id']
        item = items.get(item_id)
        
        if item:
            # Find inventory for this item
            inv = next((inv for inv in inventory.values() if inv['item_id'] == item_id), None)
            available = inv['quantity'] if inv else 0
            
            fulfillment_items.append({
                'id': item_id,
                'name': item['name'],
                'requested': req_item['quantity'],
                'available': available,
                'max_fulfill': min(req_item['quantity'], available)
            })
    
    return render_template('request/fulfill.html', request=req, items=fulfillment_items)

@app.route('/request/purchase', methods=['GET', 'POST'])
@role_required(['store_assistant', 'admin', 'superadmin'])
def request_purchase():
    # Get items from session
    purchase_items = session.get('purchase_items', [])
    request_id = request.args.get('request_id')
    
    if not purchase_items:
        flash('No items to purchase.')
        return redirect(url_for('request_list'))
    
    if request.method == 'POST':
        # In a real application, this would create a purchase order
        # For this demo, we'll just show a success message
        flash('Purchase request created successfully.')
        session.pop('purchase_items', None)
        return redirect(url_for('request_list'))
    
    return render_template('request/purchase.html', items=purchase_items, request_id=request_id)

if __name__ == '__main__':
    app.run(debug=True)