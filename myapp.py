from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

# Database configuration
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
version = os.getenv('VERSION')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Create the database and the table
with app.app_context():
    db.create_all()

@app.route('/user', methods=['POST'])
def new_user():
    data = request.get_json()
    new_u = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        email=data['email']
    )
    db.session.add(new_u)
    db.session.commit()
    return jsonify({
        'id': new_u.id,
        'first_name': new_u.first_name,
        'last_name': new_u.last_name,
        'age': new_u.age,
        'email': new_u.email
    }), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': user.age,
        'email': user.email
    })

@app.route('/count', methods=['GET'])
def count_users():
    count = User.query.count()
    return jsonify({'count': count})


@app.route(('/version'), methods=['GET'])
def get_version():
    return jsonify({'version': version})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)