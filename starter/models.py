import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String

db = SQLAlchemy()


def setup_db(app):
    """
    Connect to database using the config file values
    :param app:
    :return:
    """

    app.config.from_object('config')
    db.app = app
    db.init_app(app)


class Movies(db.Model):
    """
    Create movie table
    """
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    release_date = db.Column(db.Date)
    #
    # casting = db.relationship('Casting', backref='Movies', lazy=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {'id': self.id,
                'title': self.title,
                'release_date': self.release_date}


class Actors(db.Model):
    """
    Create actor table
    """
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    # casting = db.relationship('Casting', backref='Movies', lazy=True)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {'id': self.id,
                'name': self.name,
                'age': self.age,
                'gender': self.gender
                }

#
# class Casting(db.Model):
#     """
#     casting table
#     """
#     __tablename__ = 'casting'
#     id = db.Column(db.Integer, primary_key=True)
#     movies_id = db.Column(db.Integer,
#                           db.ForeignKey('movie.id'), nullable=False)
#     actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'),
#                          nullable=False)
#
#     def add(self):
#         db.session.add(self)
#         db.session.commit()
#
#     def delete(self):
#         db.session.delete(self)
#
#     def update(self):
#         db.session.commit()
#
#     def format(self):
#         return {'id': self.id,
#                 'movies_id': self.movies_id,
#                 'actor_id': self.actor_id}

