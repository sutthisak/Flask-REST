from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

import resources

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

'''db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()
'''

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
#app.config['JWT_BLACKLIST_ENABLED'] = True
#app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
api.add_resource(resources.Item, '/item/<string:name>')
api.add_resource(resources.ItemList, '/items')

app.run(port=5000, debug=True)
