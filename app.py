import psycopg2
import sys
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from config import db, DATABASE_URL


app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

from model import PasswordModel
migrate = Migrate(app, db)

@app.route('/')
@cross_origin(origin='http://localhost:port',headers=['Content-Type','Authorization'])
def hello():
    return "jean", 200

# request /cars pour ajouter une car et pour afficher
@app.route('/cars', methods=['POST', 'GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_car = CarsModel(name=data['name'], model=data['model'], doors=data['doors'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"car {new_car.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]

        return {"count": len(results), "cars": results}

if __name__ == '__main__':
    app.run(debug=True)