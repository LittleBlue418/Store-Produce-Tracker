import sqlite3
from db import db

class ItemModel(db.Model):
    # Setting up SQLAlchemy table
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}


    # Moving code that we re-use out into a class method,
    # this is used by both get & post
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
            # SELECT * FROM items WHERE name=argument, give us the first
            # returns an item model object


    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()


    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # Without the WHERE name=? it would update ALL prices!
        query = "UPDATE items SET price=? WHERE name=?"
        # Arguments in the tuple must be in the correct order
        # Whichever question mark is first, that argument first etc
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()