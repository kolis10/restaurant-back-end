from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# class Users(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(40))
#     last_name = db.Column(db.String(40))
#     order_time = db.Column(db.String(120))

#     orders = db.relationship('Orders', back_populates='user')

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "first_name": self.first_name,
#             "last_name": self.last_name,
#             "order_time": self.order_time,
#             "orders": [x.serialize() for x in self.orders]
#         }

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    final_price = db.Column(db.Float)
    
    foods = db.relationship('Foods', back_populates='order')

    def __repr__(self):
        return '<Orders %r>' % self.achievement

    def serialize(self):
        return {
            "id": self.id,
            "order": [x.serialize() for x in self.foods],
            "name": self.name,
            "time": self.time
        }

class Foods(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    food = db.Column(db.String(500))
    price = db.Column(db.Float)
    
    order = db.relationship('Orders', back_populates='foods')

    def __repr__(self):
        return '<Foods %r>' % self.foods

    def serialize(self):
        return {
            "order_id": self.order_id,
            "food": self.food,
            "price": self.price
        }

# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.username

#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }