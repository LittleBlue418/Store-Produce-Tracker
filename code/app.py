# Importing from flask and flask libraries
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# Importing our security
from security import authenticate, identity

# Importing from within the project
from db import db
from resources.user import UserRegister
from resources.item import Item, ItemList


# Set up our Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'

# Set up our API
api = Api(app)

# Set up our JavaScript Web Token
jwt = JWT(app, authenticate, identity)

# Initializing our SQLAlchemy database
db.init_app(app)


# Creating the tables in our data.db file (runs once)
@app.before_first_request
def create_tables():
    db.create_all()


# Initializing our API end points.
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


# If this code is running in the main file (not via imported)
# Initializing the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
