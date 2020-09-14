from flask import Flask
from accounts import accounts
from auth import auth
from deposits import deposits
from withdraws import withdraws
from transfers import transfers

app = Flask(__name__)
app.register_blueprint(accounts)
app.register_blueprint(auth)
app.register_blueprint(deposits)
app.register_blueprint(withdraws)
app.register_blueprint(transfers)

if __name__ == '__main__':
    app.run(debug=True)
