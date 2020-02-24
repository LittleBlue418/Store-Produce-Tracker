# Importing from flask and flask libraries
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

# Importing from security, which itself imports from
# our user class file
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

# Set up
app = Flask(__name__)
app.secret_key = 'key'
api = Api(app)
db.init_app(app)
jwt = JWT(app, authenticate, identity)


# Initializing and establishing our end points. Note that we group
# end points by class, so because the post and put etc target a
# single item we can put them in a single class, but because get
# items has a different end point it has it's own class
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


# If this code is running in the main file (not via imported)
# Initializing the app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
