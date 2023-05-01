from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)

app.secret_key = 'asdfghjklm'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'var31'
app.config['MYSQL_DB'] = 'db2'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'var31'
# app.config['MYSQL_DB'] = 'aint'

mysql = MySQL(app)
