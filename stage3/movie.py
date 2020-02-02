import sqlite3

from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Movie(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument(
    #     "name", type=str, required=True, help="This field cannot be left blank!"
    # )
    parser.add_argument(
        "genre", type=str, required=True, help="This field cannot be left blank!"
    )

    # @jwt_required()
    def get(self, name):
        movie = MovieClass.find(name)
        if movie:
            return {"name": movie.name, "genre": movie.genre}
        return {"message": "There is no movie with such a title."}, 418

    # @jwt_required()
    def post(self, name):
        movie = MovieClass.find(name)
        print(movie)
        if movie:
            print(name)
            return {"message": "Movie titled like this already exists."}, 400
        data = Movie.parser.parse_args()
        movie = MovieClass.save(name=name, genre=data["genre"])
        return movie, 201

    # @jwt_required()
    def delete(self, name):
        movie = MovieClass.find(name)
        if movie:
            movie.delete()
            return {"message": "movie deleted"}, 204

        return {"message": "Movie titled like this does not exist."}, 400

    def put(self, name):
        data = Movie.parser.parse_args()
        genre = data["genre"]
        movie = MovieClass.find(name)
        status = 201

        if not movie:
            # movie = MovieClass(name, genre)
            movie = MovieClass.save(name=name, genre=genre)
        else:
            movie.update()
            status = 202

        # return movie.to_dict(), status
        # return {'name': movie.name, 'genre': movie.genre}, status
        return {'message': 'Movie updated.'}, status


class MovieList(Resource):
    # @jwt_required()
    def get(self):
        # return {"movies": [movie.to_dict() for movie in MovieClass.get_all()]}
        return {"movies": [{'name': movie.name, 'genre': movie.genre} for movie in MovieClass.get_all()]}


class MovieClass:
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre

    @classmethod
    def find(cls, searchphrase, searchtype="name"):
        query = f"SELECT * FROM movies WHERE name = ?"
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        result = cursor.execute(query, (searchphrase, ))
        row = result.fetchone()
        movie = None
        if row:
            movie = MovieClass(row[0], row[1])
        connection.close()
        return movie

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
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM movies WHERE name = ?"
        cursor.execute(query, (self.name, ))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE movies SET genre = ? WHERE name = ?"
        cursor.execute(query, (self.name, self.genre))
        connection.commit()
        connection.close()

    @classmethod
    def get_all(cls):
        movies = []
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM movies"
        result = cursor.execute(query)
        for element in result:
            movies.append(cls(element[0], element[1]))
        connection.commit()
        connection.close()
        return movies
