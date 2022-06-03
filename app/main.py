from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)

cars = {1: {'brand': 'Ford', 'model': 'Mustang', 'year': 1990, 'hp': 300, 'color': 'red'},
        2: {'brand': 'Ford', 'model': 'Mondeo', 'year': 2015, 'hp': 200, 'color': 'gold'},
        3: {'brand': 'Mazda', 'model': 'CX5', 'year': 2010, 'hp': 300, 'color': 'black'},
        4: {'brand': 'Mercedes-Benz', 'model': 'C Klasse', 'year': 2004, 'hp': 150, 'color': 'violet'}
        }


# cars = {1: {'brand': 'Ford'},
#         2: {'brand': 'Ford2'},
#         3: {'brand': 'Mazda'},
#         4: {'brand': 'Mercedes-Benz'}
#         }

car_parser = reqparse.RequestParser()
car_parser.add_argument('brand', help="Brand cannot be empty!")
car_parser.add_argument('model')
car_parser.add_argument('year', type=int)
car_parser.add_argument('hp', type=int)
car_parser.add_argument('color')



class Car(Resource):
    def get(self, id):
        if id not in cars:
            return {}
        item = {}
        item[int(id)] = cars[int(id)]
        return item
        
    def delete(self, id):
        del cars[int(id)]
        return '', 204
    
    def put(self, id):
        args = car_parser.parse_args()
        cars[int(id)] = {'brand': args['brand'], 'model': args['model'], 'year': args['year'], 'hp': args['hp'], 'color': args['color']}
        # cars[int(id)] = {'brand': args['brand']}
        return cars[int(id)], 201
        

class Cars(Resource):
    def get(self):
        return cars
    
    def post(self):
        args = car_parser.parse_args()
        id = int(max(cars.keys())) + 1
        cars[id] = {'brand': args['brand'], 'model': args['model'], 'year': args['year'], 'hp': args['hp'], 'color': args['color']}
        # cars[id] = {'brand': args['brand']}
        return cars[id], 201
    
class Brand(Resource):
    def get(self, brand):
        
        # print([car for car in cars.values() if brand.lower() in car['brand'].lower()])
        # return [car for car in cars.values() if brand.lower() in car['brand'].lower()]
        
        brand_items = {}
        for id in cars:
            if brand.lower() in cars[id]['brand'].lower():
                brand_items[id] = cars[id]
        return brand_items
    
    
api.add_resource(Cars, '/cars/')
api.add_resource(Car, '/cars/<id>/')
api.add_resource(Brand, '/cars/brand/<brand>/')

