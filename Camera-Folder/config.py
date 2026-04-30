from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# Initializes flask application
app = Flask(__name__)
CORS(app) # resolves cross origin errors

# Database config (Not 100%, will need an actual URL to connect to the DB)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:password@localhost/flask_db'

# Makes the instance of the database
db = SQLAlchemy(app)



class Testing(db.Model):
    """
    The database model but represented as a modifiable class
    """


