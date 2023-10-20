from flask import Flask
from flask_mysqldb import MySQL
import re

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key'

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'pass'
    app.config['MYSQL_DB'] = 'SSISv3'

    mysql.init_app(app)

    from .views import views
    from .change import change
    from .create import create
    from .delete import delete

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(change, url_prefix='/')
    app.register_blueprint(create, url_prefix='/')
    app.register_blueprint(delete, url_prefix='/')

    return app
