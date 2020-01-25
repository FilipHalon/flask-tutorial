from flask import Flask, request
from flask_restful import Resource, Api, reqparse
# Resource - reprezentacja jakiegoś konkretnego bytu; zazwyczaj ma odzwierciedlenie w tabeli
from flask_jwt import JWT, jwt_required


from security import authenticate, identity

movies = []

app = Flask(__name__)
api = Api(app)
# klucz do szyfrowania; najważniejsze dla JWT
app.secret_key = "cokolwiek"
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)
# jwt tworzy nowy endpoint /auth


class Student(Resource):
    # dostępne są również post, update, delete
    def get(self, name):
        return {'student': name}


class Movie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "genre", type=str, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        for movie in movies:
            if movie["name"] == name:
                return movie
        return {"message": "filmu nie znaleziono"}, 418

    def post(self, name):
        data = request.get_json(silent=True) # jest jeszcze force=True
        movie = {"name": name, "genre": data["genre"]}
        movies.append(movie)
        print(movies)
        return movie, 201

    def delete(self, name):
        global movies
        movies = [movie for movie in movies if movie["name"] != name]
        return {"message": "movie deleted"}, 204

    def put(self, name):
        # data = request.get_json()
        data = Movie.parser.parse_args()

        movie = None
        status = 200

        for _movie in movies:
            if _movie["name"] == name:
                movie = _movie

        if movie is None:
            movie = {"name": name, "genre": data["genre"]}
            movies.append(movie)
        else:
            movies.update(data)
            status = 204

        return movie, status


class MovieList(Resource):
    # @jwt_required()
    def get(self):
        return {"movies": movies}


api.add_resource(Student, '/student/<string:name>')
api.add_resource(Movie, '/movie/<string:name>')
api.add_resource(MovieList, '/movies')
app.run(debug=True)
