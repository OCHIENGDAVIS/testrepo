# this app is super genius
import sqlite3
from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister
app = Flask(__name__)
api = Api(app)
app.secret_key = "awerdgfhjkllo"
jwt = JWT(app, authenticate, identity)
items = [

]

#
# @app.route('/')
# def home():
#     return "Hello there"
#
# # POST /store data <name>/
# # POST /store/<string:name>/item
# # GET /store/<string:name>
# # GET /stores/
#
# @app.route('/store', methods=['POST'])
# def create_store():
#     pass
#
# @app.route('/store/<string:name>')
# def get_store(name):
#     pass
#
# @app.route('/stores')
# def get_stores():
#     return jsonify({'stores': stores})
#
#
# @app.route('/store/<string:name>/item', methods=['POST'])
# def create_item_in_store():
#     pass
#
#
# @app.route('/store/<string:name>/item')
# def get_item_in_store(name):
#     pass



class Items(Resource):
    # @jwt_required()
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'message': 'item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM "


    # @jwt_required()
    def post(self, name):
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] !=name, items))
        return {'message' : 'item deleted'}

    def put(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float,required=True, help='filed cant be blank')
        data = parser.parse_args()
        item = next(filter(lambda x: x['name']==name, items), None)
        if item is None:
            item = {"name": name, "price" : data['price']}
            items.append(item)
        else:
            item.update(data)



class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {'items': items}



api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')



if __name__ == "__main__":
    app.run(debug=True)