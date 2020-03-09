import os

# Importing from flask and flask libraries
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

# Importing from within the project
from db import db
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList


# Set up our Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'key'

# Set up our API
api = Api(app)

# Set up our JavaScript Web Token
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 3: # 'user 3' used to match postman for testing
        return {'is_admin': True}
    return {'is_admin': False}


# JWT config responses
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature varification failed',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain and access token.',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


# Initializing our SQLAlchemy database
db.init_app(app)


# Creating the tables in our data.db file (runs once)
@app.before_first_request
def create_tables():
    db.create_all()


# Initializing our API end points.
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')


# If this code is running in the main file (not via imported)
# Initializing the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
