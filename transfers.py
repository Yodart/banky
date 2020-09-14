from flask import Flask, Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

transfers = Blueprint('transfers', __name__)


@ transfers.route('/transfer', methods=['POST'])
@db_connect
@require_auth_token
def create_transfer(current_account, db_cursor, db_connection):
    sender_account_number = current_account['account_number']
    reciever_account_number = request.json['reciever_account_number']
    ammount = request.json['ammount']
    try:
        db_cursor.execute(
            "SELECT balance FROM accounts WHERE account_number=%s", ([sender_account_number]))
        if ammount > db_cursor.fetchall()[0][0]:
            return jsonify({'error': 'Insuficient Funds!'}), 401
        db_cursor.execute(
            "INSERT INTO transfers (ammount,sender_account_number,reciever_account_number) values(%s,%s,%s)", (ammount, sender_account_number, reciever_account_number))
        db_cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (ammount, sender_account_number))
        db_cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (ammount, reciever_account_number))
        db_connection.commit()
        return jsonify({'message': 'Transfer completed'}), 200
    except:
        return {'error': "Unable to make transfer", "traceback": str(sys.exc_info())}, 401


@ transfers.route('/transfer/<int:transfer_id>', methods=['GET'])
@db_connect
@require_auth_token
def query_single_transfer(current_account, db_cursor, db_connection, transfer_id):
    try:
        db_cursor.execute(
            "SELECT id,sender_account_number,reciever_account_number,ammount,timestamp FROM transfers WHERE id=%s AND sender_account_number = %s LIMIT 1", (transfer_id, current_account['account_number']))
        transfer_data = db_cursor.fetchall()[0]
        return {'id': transfer_data[0],
                'sender_account_number': transfer_data[1],
                'reciever_account_number': transfer_data[2],
                'ammount': transfer_data[3],
                'timestamp': transfer_data[4]}, 200
    except:
        return {'error': "Unable to fetch /transfer/<id>", "traceback": str(sys.exc_info())}, 401


@ transfers.route('/transfers', methods=['GET'])
@db_connect
@require_auth_token
def query_transfers(current_account, db_cursor, db_connection):
    acc_number = current_account['account_number']
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    try:
        db_cursor.execute(
            "SELECT id,sender_account_number,reciever_account_number,ammount,timestamp FROM transfers WHERE sender_account_number = %s LIMIT %s OFFSET %s", (acc_number, limit, offset))
        transfers = []
        for transfer in db_cursor.fetchall():
            transfers.append({'id': transfer[0],
                              'sender_account_number': transfer[1],
                              'reciever_account_number': transfer[2],
                              'ammount': transfer[3],
                              'timestamp': transfer[4]})
        return jsonify({'transfers': transfers}), 200
    except:
        return {'error': "Unable to fetch /transfers/<acc_number>", "traceback": str(sys.exc_info())}, 401
