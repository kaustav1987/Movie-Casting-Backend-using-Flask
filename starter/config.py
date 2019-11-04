import os

# Set debug Mode to True for development
DEBUG = True

# Connect to database
#You should create the database name casting_agency
database_name = 'casting_agency'
# # I have created a user name Kaustav with password k
database_path = 'postgres://{}:{}@{}/{}'.format('Kaustav', 'k',
                                               'localhost:5432', database_name)

# DATABASE URL
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = database_path

