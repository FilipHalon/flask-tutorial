import sqlite3
from db import db


class MovieModel(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    genre = db.Column(db.String(128))

    def __init__(self, name, genre):
        self.name = name
        self.genre = genre

    @classmethod
    def get_movie_by_name(cls, name):
        return MovieModel.query.filter_by(name=name).first()

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def save(cls, name, genre):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO movies VALUES (?, ?)"
        cursor.execute(query, (name, genre))
        connection.commit()
        connection.close()
        return {"message": "Movie created."}, 201

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE movies SET genre = ? WHERE name = ?"
        cursor.execute(query, (self.name, ))
        connection.commit()
        connection.close()

    @classmethod
    def get_all(cls):
        return MovieModel.query.all()
