"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_simple import JWTManager, create_jwt, jwt_required
from utils import APIException, generate_sitemap
from models import db, Orders, Foods
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/customer', methods=['POST','GET'])
def customer():

    json = request.get_json()
    client = Orders(
        name = json['name']
    )
    db.session.add(client)
    db.session.commit()

    final_price = 0

    for x in json['order']:
        db.session.add(Foods(
            food = x['food'],
            price = x['price'],
            order_id = client.id
        ))
        final_price += x['price']

    client.final_price = final_price
    db.session.commit()

    return jsonify( Orders.query.get(client.id).serialize() )

@app.route('/login', methods=['POST'])
def login():

    json = request.get_json()

    user = Orders.query.filter_by(
        name = json['name']
    ).first()

    if user is None:
        raise APIException('User Not Found: 404')

    return jsonify(create_jwt(identity=json['name']))


@app.route('/salute')
@jwt_required
def salute():
    return 'hello Issac'

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
