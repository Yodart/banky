from flask import Blueprint
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import Database
import datetime
import jwt

auth_service = Blueprint('auth', __name__)
db = Database("todoodledb")


def require_auth_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'error': 'Missing auth token'}), 401
        try:
            data = jwt.decode(token, 'secret')
            current_user = db.get_single_user_by_id(user_id=[data['id']])
        except:
            return jsonify({'error': 'Invalid auth token.'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@auth_service.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login requited!"'})
    user = db.get_single_user_by_name(name=[auth.username])
    if check_password_hash(user['password'], auth.password):
        print(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))
        token = jwt.encode(
            {'id': user['id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'secret')
        return jsonify({'token': token.decode('UTF-8')})
    return {'message': "Wrong Password"}
