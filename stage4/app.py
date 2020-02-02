from flask import Flask, request
from flask_restful import Resource, Api, reqparse
# Resource - reprezentacja jakiegoś konkretnego bytu; zazwyczaj ma odzwierciedlenie w tabeli
from flask_jwt import JWT, jwt_required


from security import authenticate, identity
from resources.user import UserRegister
from resources.movie import Movie, MovieList

movies = []

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
# klucz do szyfrowania; najważniejsze dla JWT
app.secret_key = "cokolwiek"
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)
# jwt tworzy nowy endpoint /auth


class Student(Resource):
    # dostępne są również post, update, delete
    def get(self, name):
        return {'student': name}


api.add_resource(Student, '/student/<string:name>')
api.add_resource(Movie, '/movie/<string:name>')
api.add_resource(MovieList, '/movies')
api.add_resource(UserRegister, '/user/register')
app.run(debug=True)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run()
