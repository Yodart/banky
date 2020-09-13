from flask import Flask
from accounts import accounts
from auth import auth
from deposits import deposits

app = Flask(__name__)
app.register_blueprint(accounts)
app.register_blueprint(auth)
app.register_blueprint(deposits)

if __name__ == '__main__':
    app.run(debug=True)
