from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

DB_URI = "postgresql:///restful_api"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = SQLAlchemy(app)
ma = Marshmallow(app)

# SQLALCHEMY_TRACK_MODIFICATIONS = False
# To create the initial database, just import the db object from an interactive Python shell 
# and run the SQLAlchemy.create_all() method to create the tables and database:

# >>> from crud import db
# >>> db.create_all()

db.init_app(app)


class User(db.Model):
    # user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<User username={} email={}>".format(self.username, self.email)

class UserSchema(ma.Schema):
    class Meta:
        fileds = ('username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

#endpoint to create users
@app.route("/")
def hello():
    return "Hello Sam"

@app.route("/user", methods=["POST"])
def add_user():
    # username = request.form.get('username')
    # email = request.form.get('email')

    username = request.json['username']
    email = request.json['email']

    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    print new_user
    

    return user_schema.jsonify(new_user)


@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    # need explaination
    return jsonify(result.data)


@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
    user=User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    