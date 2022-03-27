from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import credentials
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('config.py')
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = credentials.host
app.config['MYSQL_USER'] = credentials.user
app.config['MYSQL_PASSWORD'] = credentials.passwd
app.config['MYSQL_DB'] = credentials.db_name

mysql = MySQL(app)

db = SQLAlchemy(app)

from route import *

if __name__ == '__main__':
	port = int(os.environ.get("BACKEND_PORT", 5000))
	app.run(host="0.0.0.0", port=port)
