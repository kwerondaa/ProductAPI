from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

#initialize the application. instatiate an object
app = Flask(__name__)

#letting the server kno where the database file is.
basedir = os.path.abspath(os.path.dirname(__file__))

#setting up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)

#initialize marshmallow
ma = Marshmallow(app)


#Product/Model/Resource
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#create schema structures
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'description', 'price', 'qty')

#initialize schemas
product_schema = ProductSchema(strict = True)
products_schema = ProductSchema(many = True, strict = True)


#creating routes
#adding a product
@app.route('/product', methods =['GET'])
def new_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#getting a product
@app.route('/product/<id>', methods = ['GET'])
def get_a_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

#getting all products
@app.route('/product', methods = ['GET'])
def get_all_products():
    products = Product.query(all)
    result = products_schema.dump(products)
    return jsonify(result.data)


#updating a product
@app.route('/product/<id>', methods = ['PUT'])
def update_product(id):
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()
    return product_schema.jsonify(product)

#deleting a product
@app.route('/product/<id>', methods = ['DELETE'])
def delete_product(id):

    product = Product.query.get(id)

    db.session.delete(product)
    return product_schema.jsonify(product)




#to run the server
if __name__ == "__main__":
    app.run(debug= True)