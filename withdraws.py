from flask import Flask, Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

withdraws = Blueprint('withdraws', __name__)


@ withdraws.route('/withdraw', methods=['POST'])
@db_connect
@require_auth_token
def create_withdraw(current_account, db_cursor, db_connection):
    account_number = current_account['account_number']
    ammount = request.json['ammount']
    try:
        db_cursor.execute(
            "SELECT balance FROM accounts WHERE account_number=%s", ([account_number]))
        if ammount > db_cursor.fetchall()[0][0]:
            return jsonify({'error': 'Insuficient Funds!'}), 401
        db_cursor.execute(
            "INSERT INTO withdraws (ammount,account_number) values(%s,%s)", (ammount, account_number))
        db_cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (ammount, account_number))
        db_connection.commit()
        return jsonify({'message': 'Ammounted Withdrawed!'}), 200
    except:
        return {'error': "Unable to make withdraw", "traceback": str(sys.exc_info())}, 401


@ withdraws.route('/withdraw/<int:withdraw_id>', methods=['GET'])
@db_connect
@require_auth_token
def query_single_withdraw(current_account, db_cursor, db_connection, withdraw_id):
    try:
        db_cursor.execute(
            "SELECT id,account_number,ammount,timestamp FROM withdraws WHERE id=%s AND account_number = %s LIMIT 1", (withdraw_id, current_account['account_number']))
        account_data = db_cursor.fetchall()[0]
        return {'id': account_data[0],
                'account_number': account_data[1],
                'ammount': account_data[2],
                'timestamp': account_data[3]}, 200
    except:
        return {'error': "Unable to fetch /withdraw/<id>", "traceback": str(sys.exc_info())}, 401


@ withdraws.route('/withdraws/', methods=['GET'])
@db_connect
@require_auth_token
def query_withdraws(current_account, db_cursor, db_connection):
    acc_number = current_account['account_number']
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    try:
        db_cursor.execute(
            "SELECT id,account_number,ammount,timestamp FROM withdraws WHERE account_number = %s LIMIT %s OFFSET %s", (acc_number, limit, offset))
        withdraws = []
        for withdraw in db_cursor.fetchall():
            withdraws.append({'id': withdraw[0],
                              'account_number': withdraw[1],
                              'ammount': withdraw[2],
                              'timestamp': withdraw[3]})
        return jsonify({'withdraws': withdraws}), 200
    except:
        return {'error': "Unable to fetch /withdraws/<acc_number>", "traceback": str(sys.exc_info())}, 401
