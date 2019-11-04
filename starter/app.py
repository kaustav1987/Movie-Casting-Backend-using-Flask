import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_moment import Moment
from flask_migrate import Migrate
from models import Movies, Actors, setup_db,  db
from auth import requires_auth, AuthError


# print(sys.path)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    moment = Moment(app)
    CORS(app)

    # Connect to database
    setup_db(app)

    # Using migrate for scalability of the database to accommodate
    # database changes without loosing data
    # db.create_all()
    migrate = Migrate(app, db)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        # Exclude PUT method
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def index():
        return 'Welcome to Actor Casting App'

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        # I am doing to check the authorization using decorator.
        # So I am defining different methods
        # if request.method == "GET":
        try:
            actors = Actors.query.all()
            all_actors = [actor.format() for actor in actors]
            return jsonify({'success': True,
                            'actors': all_actors}), 200
        except:
            abort(404)

    @app.route('/movies', methods= ['GET'])
    @requires_auth('get:movies')
    def get_movies():
        try:
            movies = Movies.query.all()
            all_movies = [movie.format() for movie in movies]
            return jsonify({'success': True,
                            'movies': all_movies}), 200
        except:
            abort(404)

    @app.route('/actors/<actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_specific_actors(actor_id):
        try:
            actor = Actors.query.get(actor_id)
            return jsonify({'success': True,
                            'actors': [actor.format()]}), 200
        except:
            abort(404)

    @app.route('/movies/<movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_specific_movies(movie_id):
        try:
            movie = Movies.query.get(movie_id)
            return jsonify({'success': True,
                            'movies': [movie.format()]}), 200
        except:
            abort(404)

    @app.route('/actors', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor():

        try:
            data = request.get_json()
            actor_id = data.get('id', None)
            actor = Actors.query.get(actor_id)
            actor.delete()
            return jsonify({'success': True,
                            'actors': [actor.id]}), 200
        except:
            abort(404)

    @app.route('/actors/<actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor_with_parms(actor_id):
        try:
            # data = request.get_json()
            actor = Actors.query.get(actor_id)
            actor.delete()
            return jsonify({'success': True,
                            'actors': [actor.id]}), 200
        except:
            abort(404)

    @app.route('/movies', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies():
        try:
            data = request.get_json()
            movies_id = data.get('id', None)
            movie = Movies.query.get(movies_id)
            movie.delete()
            return jsonify({'success': True,
                            'movies': [movie.id]}), 200
        except:
            abort(404)

    @app.route('/movies/<movies_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies_with_parms(movies_id):
        try:
            # data = request.get_json()
            movie = Movies.query.get(movies_id)
            movie.delete()
            return jsonify({'success': True,
                            'movies': [movie.id]}), 200
        except:
            abort(404)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors():
        try:
            data = request.get_json()
            print(data)
            name = data.get('name', None)
            age = data.get('age', None)
            gender = data.get('gender', None)
            actor = Actors(name=name,
                           age=age,
                           gender=gender)
            actor.add()
            return jsonify({'success': True,
                            'actors': [actor.format()]}), 200
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies():
        try:
            data = request.get_json()
            title = data.get('title', None)
            release_date = data.get('release_date', None)
            movie = Movies(title=title, release_date=release_date)
            movie.add()
            return jsonify({'success': True,
                            'movies': [movie.format()]}), 200
        except:
            abort(422)

    @app.route('/actors', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors():
        data = request.get_json()
        id = data.get("id", None)
        if id is None:
            abort(404)

        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        try:
            actor = Actors.query.get(id)

            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender

            actor.update()

            return jsonify({'success': True,
                                'actors': [actor.format()]}), 200
        except:
            abort(422)

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors_with_id_parms(id):
        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)

        try:
            actor = Actors.query.get(id)

            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender

            actor.update()

            return jsonify({'success': True,
                                'actors': [actor.format()]}), 200
        except:
            abort(422)

    @app.route('/movies', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies():
        data = request.get_json()
        id = data.get("id", None)
        if id is None:
            abort(404)

        title = data.get('title', None)
        release_date = data.get('release_date', None)

        try:
            movie = Movies.query.get(id)
        except:
            abort(404)
        try:
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date

            movie.update()
            return jsonify({'success': True,
                            'movies': [movie.format()]}), 200
        except:
            abort(422)

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies_with_id_parms(id):
        data = request.get_json()

        title = data.get('title', None)
        release_date = data.get('release_date', None)

        try:
            movie = Movies.query.get(id)
        except:
            abort(404)
        try:
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date

            movie.update()
            return jsonify({'success': True,
                            'movies': [movie.format()]}), 200
        except:
            abort(422)



    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            "error": 422,
            "message": "Unprocessable"}), 422

    @app.errorhandler(401)
    def authorization_malformed(error):
        return jsonify(
            {"success": False,
             "error": 401,
             "message": "Authorization malformed"}
        ), 401

    @app.errorhandler(400)
    def invalid_token(error):
        return jsonify(
            {"success": False,
             "error": 400,
             "message": "invalid token"}
        ), 400

    return app


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000, debug=True)
