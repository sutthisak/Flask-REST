from werkzeug.security import safe_str_cmp
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token,
        jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class User:
    def __init__(self, uid, username, password):
        self.uid = uid
        self.username = username
        self.hash_password = sha256.hash(password)

    @staticmethod
    def authenticate(username, password):
        user = username_mapping.get(username, None) # Get the value of uname key, If not found then return None
        if user and sha256.verify(password, user.hash_password):
            access_token = create_access_token(identity = user.username)
            refresh_token = create_refresh_token(identity = user.username)
            return {
                'message': 'Logged in as {}'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 200
        else:
            return { "message": "Wrong credentials" }, 401

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'uid': x.uid,
                'username': x.username,
                'hash_password': x.hash_password
            }
        return { 'users': list(map(lambda x: to_json(x), users)) }

users = [ User(1, 'bank', 'bank'), User(2, 'bang', 'bang') ] # In memory user db
username_mapping = { u.username: u for u in users }
userid_mapping = { u.uid: u for u in users }
