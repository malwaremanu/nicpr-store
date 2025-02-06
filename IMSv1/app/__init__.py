from flask import Flask
from odeta import localbase

db = localbase('test.db')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    with app.app_context():
        from .routes import auth, indent, inventory, user, master
        app.register_blueprint(auth.bp)
        app.register_blueprint(indent.bp)
        app.register_blueprint(inventory.bp)
        app.register_blueprint(user.bp)
        app.register_blueprint(master.bp)

    return app