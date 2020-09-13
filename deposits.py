from flask import Flask, Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

deposits = Blueprint('deposits', __name__)


@ deposits.route('/deposit', methods=['POST'])
@db_connect
@require_auth_token
def create_deposit(current_account, db_cursor, db_connection):
    account_number = request.json['account_number']
    ammount = request.json['ammount']
    try:
        db_cursor.execute(
            "INSERT INTO deposits (ammount,account_number) values(%s,%s)", (ammount, account_number))
        db_cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (ammount, account_number))
        db_connection.commit()
        return jsonify({'message': 'Ammounted Deposited!'}), 200
    except:
        return {'error': "Unable to make deposit", "traceback": str(sys.exc_info())}, 401


@ deposits.route('/deposit/<int:deposit_id>', methods=['GET'])
@db_connect
@require_auth_token
def query_single_deposit(current_account, db_cursor, db_connection, deposit_id):
    try:
        db_cursor.execute(
            "SELECT id,account_number,ammount,timestamp FROM deposits WHERE id=%s AND account_number = %s LIMIT 1", (deposit_id, current_account['account_number']))
        account_data = db_cursor.fetchall()[0]
        return {'id': account_data[0],
                'account_number': account_data[1],
                'ammount': account_data[2],
                'timestamp': account_data[3]}, 200
    except:
        return {'error': "Unable to fetch /deposit/<id>", "traceback": str(sys.exc_info())}, 401


@ deposits.route('/deposits/<int:acc_number>', methods=['GET'])
@db_connect
@require_auth_token
def query_deposits(current_account, db_cursor, db_connection, acc_number):
    if current_account['account_number'] != acc_number:
        return jsonify({"error": "Sensity user data, please log into the account"}), 401
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    try:
        db_cursor.execute(
            "SELECT id,account_number,ammount,timestamp FROM deposits WHERE account_number = %s LIMIT %s OFFSET %s", (acc_number, limit, offset))
        deposits = []
        for deposit in db_cursor.fetchall():
            deposits.append({'id': deposit[0],
                             'account_number': deposit[1],
                             'ammount': deposit[2],
                             'timestamp': deposit[3]})
        return jsonify({'deposits': deposits}), 200
    except:
        return {'error': "Unable to fetch /deposits/<acc_number>", "traceback": str(sys.exc_info())}, 401
