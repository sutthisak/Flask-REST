from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required,
        get_jwt_identity, create_access_token)
import models

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        return {'message': 'User registration'}

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        return models.User.authenticate(data['username'], data['password'])

class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}

class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
        
class AllUsers(Resource):
    def get(self):
        return models.User.return_all()
        #return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}

class SecretResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return { 'user': current_user, 'answer': 42 }

items = []

class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x:x['name'] == name, items), None)
        return {'item':item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x:x['name'] == name, items), None):
            return {'message':'An item with name {} already exist'.format(name)}, 400 # Bad request
        data = request.get_json()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201    # Created

class ItemList(Resource):
    def get(self):
        return {'items':items}
