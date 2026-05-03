from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# Initializes flask application
app = Flask(__name__)
CORS(app) # resolves cross origin errors

# Database config (Not 100%, will need an actual URL to connect to the DB)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/vision_project'

# Makes the instance of the database
db = SQLAlchemy(app)



class Testing(db.Model):
    """
    The database model but represented as a modifiable class
    """
    __tablename__ = 'detection_logs'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime)

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Queries the database for all logs
        logs = Testing.query.all()
        # Converts the list of objects into JSON
        return jsonify([{
            "id": log.id,
            "label": log.label,
            "confidence": log.confidence,
            "status": log.status,
            "timestamp": log.timestamp
        } for log in logs]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Ensures the 'detection_logs' table exists
    print("Server starting on http://127.0.0.1:5000")
    app.run(debug=True)