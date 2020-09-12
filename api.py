import json
import uuid
import datetime
import jwt
import sys
from flask import Flask, request, jsonify, make_response
from db import Database
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from auth_service import auth_service, require_auth_token
from user_service import user_service

app = Flask(__name__)
app.register_blueprint(auth_service)
app.register_blueprint(user_service)
db = Database("bankydb")


if __name__ == '__main__':
    app.run(debug=True)
