from db import db

class ItemModel(db.Model):
    # Setting up SQLAlchemy table
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Adding in store information
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # Points at Store Model
    store = db.relationship('StoreModel')


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
            }


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
            # SELECT * FROM items WHERE name=argument, give us the first
            # returns an item model object

    @classmethod
    def find_all(cls):
        return cls.query.all()

    # Hnadles both update and add
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
