from flask import Flask
from accounts import accounts
from auth import auth
from deposits import deposits
from withdraws import withdraws
from transfers import transfers
from statement import statement

app = Flask(__name__)
app.register_blueprint(accounts)
app.register_blueprint(auth)
app.register_blueprint(deposits)
app.register_blueprint(withdraws)
app.register_blueprint(transfers)
app.register_blueprint(statement)


if __name__ == '__main__':
    app.run(debug=True)
