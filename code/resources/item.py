import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# Our items class, with the different end points as methods. Note
# that it inherrits from the Resource class.
class Item(Resource):
    # The parse functionality belongs to the class as it is shared
    # by more than one method
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    # This method has the JavaScript Web Token required decorator, the user
    # must be authenticated and have an auth key to do anything with it.
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}


    def post(self, name):
        # 'error first' - we only run the rest of the code if there are no errors.
        #  This helps us move faster, we are not loaidng things we don't need.
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        request_data = Item.parser.parse_args()

        item = ItemModel(name, request_data['price'])

        # To capture if there has been an error posting for whatever reason
        try:
            item.insert()
        except:
            return {"message": "An error occurred"}, 500

        return item, 201



    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # NB: without the 'WHERE name=?' specifying it would delete the whole table...
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}


    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, request_data['price'])

        # Using try / except will give our users nice friendly error messages
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occured inserting the item"}, 500 # always use the correct code!
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occured updating the item"}, 500
        return updated_item.json()



# A seporate class with a seporate end point to get all of the items.
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}
