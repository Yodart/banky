from flask import Blueprint
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import Database
from auth_service import require_auth_token
import datetime
import jwt


user_service = Blueprint('user', __name__)
db = Database("todoodledb")


@ user_service.route('/user', methods=['POST'])
def create_user():
    hashed_password = generate_password_hash(
        request.json['password'], method='sha256')
    return db.create_user(name=request.json['name'], password=hashed_password)


@ user_service.route('/user/<int:user_id>', methods=['GET'])
def get_single_user_by_id(user_id):
    return db.get_single_user_by_id([user_id])


@ user_service.route('/user/<int:user_id>', methods=['PUT'])
def edit_single_user(user_id):
    name = request.json['name']if 'name' in request.json else None
    password = generate_password_hash(
        request.json['password'], method='sha256') if 'password' in request.json else None
    return db.edit_user(user_id, name, password)


@ user_service.route('/user/<int:user_id>', methods=['DELETE'])
def delete_single_user(user_id):
    return db.delete_user([user_id])


@ user_service.route('/users', methods=['GET'])
def get_users():
    return db.get_users(limit=request.args.get('limit'), offset=request.args.get('offset'))
