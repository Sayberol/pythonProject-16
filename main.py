import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import raw_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


db.drop_all()
db.create_all()

for user_data in raw_data.users:
    new_user = User(
        id=user_data["id"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        age=user_data["age"],
        email=user_data["email"],
        role=user_data["role"],
        phone=user_data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()

for order_data in raw_data.orders:
    new_order = Order(
        id=order_data["id"],
        name=order_data["name"],
        description=order_data["description"],
        start_date=order_data["start_date"],
        end_date=order_data["end_date"],
        address=order_data["address"],
        price=order_data["price"],
        customer_id=order_data["customer_id"],
        executor_id=order_data["executor_id"],
    )
    db.session.add(new_order)
    db.session.commit()

for offer_data in raw_data.offers:
    new_offer = Offer(
        id=offer_data["id"],
        order_id=offer_data["order_id"],
        executor_id=offer_data["executor_id"],
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        res = []
        for u in User.query.all():
            res.append(u.to_dict())
        return json.dumps(res), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        user_data = json.load(request.data)
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.delete(new_user)
        db.session.commit()
        return "", 201


@app.route("/user/<uid>", methods=['GET', 'POST', 'DELETE'])
def get_user(uid):
    if request.method == "GET":
        return json.dumps(User.query.get(uid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        u = User.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return "", 284
    elif request.method == "PUT":
        user_data_refresh = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = user_data_refresh["first_name"],
        u.last_name = user_data_refresh["last_name"],
        u.age = user_data_refresh["age"],
        u.email = user_data_refresh["email"],
        u.role = user_data_refresh["role"],
        u.phone = user_data_refresh["phone"],
        db.session.delete(u)
        db.session.commit()
        return "", 284


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        res = []
        for o in Order.query.all():
            res.append(o.to_dict())
        return json.dumps(res), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        order_data = json.load(request.data)
        new_order = Order(
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )
        db.session.delete(new_order)
        db.session.commit()
        return "", 201


@app.route("/order/<oid>", methods=['GET', 'POST'])
def get_order(oid):
    if request.method == "GET":
        return json.dumps(Order.query.get(oid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        o = Order.query.get(oid)
        db.session.delete(o)
        db.session.commit()
        return "", 284
    elif request.method == "PUT":
        order_data_refresh = json.loads(request.data)
        o = Order.query.get(oid)
        o.name = order_data_refresh["name"],
        o.description = order_data_refresh["description"],
        o.start_date = order_data_refresh["start_date"],
        o.end_date = order_data_refresh["end_date"],
        o.address = order_data_refresh["address"],
        o.price = order_data_refresh["price"],
        o.customer_id = order_data_refresh["customer_id"],
        o.executor_id = order_data_refresh["executor_id"],
        db.session.delete(o)
        db.session.commit()
        return "", 284


@app.route("/offers", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        res = []
        for of in Offer.query.all():
            res.append(of.to_dict())
        return json.dumps(res), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        offer_data = json.load(request.data)
        new_offer = Offer(
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"],
        )
        db.session.delete(new_offer)
        db.session.commit()
        return "", 201


@app.route("/offer/<ofid>", methods=['GET', 'POST'])
def get_offer(ofid):
    if request.method == "GET":
        return json.dumps(Offer.query.get(ofid).to_dict()), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "DELETE":
        of = Offer.query.get(ofid)
        db.session.delete(of)
        db.session.commit()
        return "", 284
    elif request.method == "PUT":
        offer_data_refresh = json.loads(request.data)
        of = Offer.query.get(ofid)
        of.order_id = offer_data_refresh["order_id"],
        of.executor_id = offer_data_refresh["executor_id"],
        db.session.delete(of)
        db.session.commit()
        return "", 284


if __name__ == '__main__':
    app.run()
