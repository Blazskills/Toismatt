from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3





con = sqlite3.connect('./tmp/database.db')
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
from views import *

if __name__ =='__main__':
    app.run()
