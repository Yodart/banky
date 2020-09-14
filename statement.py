from flask import Flask, Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

statement = Blueprint('statement', __name__)


@ statement.route('/statement', methods=['GET'])
@db_connect
@require_auth_token
def query_statement(current_account, db_cursor, db_connection):
    acc_number = current_account['account_number']
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    try:
        db_cursor.execute(
            """SELECT * FROM
               (SELECT account_number, ammount,'deposit' AS type, 'null' AS reciever_account_number, timestamp FROM deposits 
                UNION ALL 
                SELECT account_number,ammount,'withdraw' AS type , 'null' AS reciever_account_number, timestamp FROM withdraws
                UNION ALL
                SELECT sender_account_number as account_number,ammount,'transfer',reciever_account_number  AS type, timestamp FROM transfers) 
                AS statement 
                WHERE statement.account_number=%s
                LIMIT %s OFFSET %s""", (acc_number, limit, offset))
        statement_items = []
        for item in db_cursor.fetchall():
            statement_items.append({'account_number': item[0],
                                    'ammount': item[1],
                                    'type': item[2],
                                    'reciever_account_number': item[3],
                                    'timestamp': item[4], })
        return jsonify({'transfers': statement_items}), 200
    except:
        return {'error': "Unable to fetch /transfers/<acc_number>", "traceback": str(sys.exc_info())}, 401
