from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
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
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )

    # This method has the JavaScript Web Token required decorator, the user
    # must be authenticated and have an auth key to do anything with it.
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}

    @fresh_jwt_required
    def post(self, name):
        # 'error first' - we only run the rest of the code if there are no errors.
        #  This helps us move faster, we are not loaidng things we don't need.
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        request_data = Item.parser.parse_args()

        item = ItemModel(name, **request_data)

        # To capture if there has been an error posting for whatever reason
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred"}, 500

        return item.json(), 201


    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}


    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']

        item.save_to_db()

        return item.json()



# A seporate class with a seporate end point to get all of the items.
class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200
        # OR return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
