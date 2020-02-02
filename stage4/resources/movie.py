import sqlite3

from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.movie import MovieModel


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
        movie = MovieModel.get_movie(name)
        if movie:
            return {"name": movie.name, "genre": movie.genre}
        return {"message": "filmu nie znaleziono"}, 418

    # @jwt_required()
    def post(self, name):
        data = Movie.parser.parse_args()
        if MovieClass.get_movie(searchphrase=name):
            return {"message": "Movie titled like this already exists."}, 400
        movie = MovieClass.save(name=name, genre=data["genre"])
        return movie, 201

    # @jwt_required()
    def delete(self, name):
        movie = MovieClass.get_movie(name)
        if movie:
            movie.delete()
            return {"message": "movie deleted"}, 204

        return {"message": "Movie titled like this already exists."}, 400

    def put(self, name):
        data = Movie.parser.parse_args()
        genre = data["genre"]
        movie = MovieClass.get_movie(name)
        status = 201

        if not movie:
            movie = MovieClass(name, genre)
            movie.save(name=name, genre=genre)
        else:
            movie.update(genre)
            status = 202

        # return movie.to_dict(), status
        return movie, status


class MovieList(Resource):
    # @jwt_required()
    def get(self):
        # return {"movies": [movie.to_dict() for movie in MovieClass.get_all()]}
        return {"movies": [movie for movie in MovieClass.get_all()]}
