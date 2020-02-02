import sqlite3
from db import db


class UserModel(db.User):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))

    def __init__(self, _id, username, password):
        # _id jest używane, żeby nie zacieniować magicznego id, metody wbudowanej pythona
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_user_by_username(cls, username):
        return UserModel.query.filter_by(name=username).first()

    @classmethod
    def find_user_by_id(cls, _id):
        return UserModel.query.filter_by(id=_id).first()
