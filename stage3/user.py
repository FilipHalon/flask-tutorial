import sqlite3

from flask import request
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        # _id jest używane, żeby nie zacieniować magicznego id, metody wbudowanej pythona
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_user_by_username(cls, username):
        query = "SELECT * FROM users WHERE username = ?"
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        user = None
        if row:
            user = User(row[0], row[1], row[2])
        # connection.commit()
        connection.close()
        return user

    @classmethod
    def find_user_by_id(cls, _id):
        query = "SELECT * FROM users WHERE id = ?"
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        user = None
        if row:
            user = User(row[0], row[1], row[2])
        # connection.commit()
        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This is required."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This is required."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_user_by_username(username=data["username"]):
            return {"message": "User with this username already exists."}, 400
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))
        connection.commit()
        connection.close()
        return {"message": "User created."}, 201


print(User.find_user_by_username(username="admin1"))
print(User.find_user_by_id(1))
