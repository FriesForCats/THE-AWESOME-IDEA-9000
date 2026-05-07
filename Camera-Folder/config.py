from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/vision_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Prevents unnecessary warnings

db = SQLAlchemy(app)

# logs table for detections (user's cart) 
class Testing(db.Model):
    __tablename__ = 'detection_logs'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=True) # Changed to True since amount was in your SQL
    status = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

# logs table for inventory 
class Inventory(db.Model):
    __tablename__ = 'inventory'
    label = db.Column(db.String(255), primary_key=True)
    amount = db.Column(db.Integer, default=0)

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Pulls the 3 most recent entries
        logs = Testing.query.order_by(Testing.id.desc()).limit(3).all()
        return jsonify([{
            "id": log.id,
            "label": log.label,
            "confidence": log.confidence,
            "status": log.status,
            "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S') if log.timestamp else None
        } for log in logs]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    try:
        # USE SQLALCHEMY instead of cursor.execute (Matches image_a7df5b.png logic)
        items = Inventory.query.all()
        inventory_data = [{"name": item.label, "stock": item.amount} for item in items]
        return jsonify(inventory_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    print("Server active on http://127.0.0.1:5000")
    app.run(debug=True)