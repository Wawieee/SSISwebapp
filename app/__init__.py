# app/__init__.py
from flask import Flask
from flask_mysqldb import MySQL
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

mysql = MySQL(app)

# Import the routes module
from app.views import routes

if __name__ == '__main__':
    app.run(debug=True)
