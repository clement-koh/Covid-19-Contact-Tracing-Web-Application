from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

# Database Settings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

# Sessions secret key
app.secret_key="mykey123"

# Database Settings
db = SQLAlchemy(app)

from . import boundary