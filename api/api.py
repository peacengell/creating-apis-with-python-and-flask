# https://medium.com/python-pandemonium/build-simple-restful-api-with-python-and-flask-part-2-724ebf04d12
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Intantiating the app with SQLALchemy and Marshmallow.
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'crud.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Create the User Class db models.


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


# Creating the UserSchema using marshmallow
class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/user/add", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']

    new_user = User(username, email)
    print(new_user)
    db.session.add(new_user)
    db.session.commit()

    msg = username + " and " + email + " added in the DB."

    return jsonify(msg)


# Endpoint to get all users.
@app.route("/user/all", methods=["GET"])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# Endpoint to get user details by id
@app.route("/user/<id>", methods=['GET'])
def get_user_by_id(id):
    user = User.query.get(id)
    if user:
        return user_schema.jsonify(user)
    else:
        return jsonify("User not Found")


#Endpoint to update user
@app.route("/user/update/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json["email"]

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# Endpoint to delete a user
@app.route("/user/delete/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)