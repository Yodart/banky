from flask import Flask, Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

accounts = Blueprint('accounts', __name__)


@ accounts.route('/account', methods=['POST'])
@db_connect
def create_account(db_cursor, db_connection):
    hashed_password = generate_password_hash(
        request.json['password'], method='sha256')
    account_number = request.json['account_number']
    name = request.json['name']
    last_name = request.json['last_name']

    try:
        db_cursor.execute(
            "SELECT id,name,last_name,account_number,balance FROM accounts WHERE account_number=%s", ([account_number]))
        account_data = db_cursor.fetchall()[0]
        return jsonify({'error': 'Account number belongs to another account'}), 401
    except:
        try:
            db_cursor.execute(
                "INSERT INTO accounts (name,last_name,password,account_number) values(%s,%s,%s,%s)", (name, last_name, hashed_password, account_number))
            db_connection.commit()
            return jsonify({'message': 'Account Created!'}), 401
        except:
            return {'error': "Unable to create account", "traceback": str(sys.exc_info())}, 401


@ accounts.route('/account/<int:acc_number>', methods=['GET'])
@db_connect
@require_auth_token
def query_single_account(current_account, db_cursor, db_connection, acc_number):
    if current_account['account_number'] != acc_number:
        return jsonify({"error": "Sensity user data, please log into the account"}), 401
    try:
        db_cursor.execute(
            "SELECT id,name,last_name,account_number,balance FROM accounts WHERE account_number=%s", ([acc_number]))
        account_data = db_cursor.fetchall()[0]
        return {'id': account_data[0],
                'name': account_data[1],
                'last_name': account_data[2],
                'account_number': account_data[3],
                'balance': account_data[4]}, 200
    except:
        return {'error': "Unable to fetch /account/<id>", "traceback": str(sys.exc_info())}, 401


@ accounts.route('/account/<int:acc_number>', methods=['PUT'])
@db_connect
@require_auth_token
def edit_account(current_account, db_cursor, db_connection, acc_number):
    if current_account['account_number'] != acc_number:
        return jsonify({"error": "Sensity user data, please log into the account"}), 401
    try:
        account = {'name': request.json['name'] if 'name' in request.json else current_account['name'],
                   'last_name': request.json['last_name'] if 'last_name' in request.json else current_account['last_name'],
                   }
        db_cursor.execute(
            "UPDATE accounts SET name = %s , last_name = %s WHERE account_number = %s", (account['name'], account['last_name'], acc_number))
        db_connection.commit()
        return {'response': 'User was edited'}, 200
    except:
        return {'error': "Unable to edit account", "traceback": str(sys.exc_info())}, 401


@ accounts.route('/account/<int:acc_number>', methods=['DELETE'])
@db_connect
@require_auth_token
def delete_account(current_account, db_cursor, db_connection, acc_number):
    if current_account['account_number'] != acc_number:
        return jsonify({"error": "Sensity user data, please log into the account"}), 401
    try:
        db_cursor.execute(
            "DELETE FROM accounts WHERE account_number = %s", ([acc_number]))
        db_connection.commit()
        return {'response': 'User deleted'}, 200
    except:
        return {'error': "Unable to delete account", "traceback": str(sys.exc_info())}


@ accounts.route('/accounts', methods=['GET'])
@db_connect
@require_auth_token
def get_accounts(current_account, db_cursor, db_connection):
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    try:
        db_cursor.execute(
            "SELECT name,last_name,account_number,created_at,balance FROM accounts ORDER BY created_at LIMIT %s OFFSET %s", (limit, offset))
        accounts = []
        for account in db_cursor.fetchall():
            accounts.append({'id': account[0],
                             'name': account[1],
                             'last_name': account[2],
                             'account_number': account[3],
                             'balance': account[4]})
        return jsonify({'accounts': accounts})
    except:
        return {'error': "Unable to fetch all accounts", "traceback": str(sys.exc_info())}
