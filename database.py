from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
from sqlalchemy import Table
# from sqlalchemy.orm import relationship

app = Flask(__name__)

DB_URL = 'postgresql://postgres:12345@localhost:5432/music_db'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

artist_genre = Table('artist_genre', db.metadata,
                     db.Column('artist_id', UUID(as_uuid=True),
                               db.ForeignKey('artist.id'), primary_key=True),
                     db.Column('genre_id', UUID(as_uuid=True), db.ForeignKey('genre.id'), primary_key=True))


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    image_url = db.Column(db.String, unique=False, nullable=True)
    mb_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4,
                      unique=True, nullable=True)
    bio = db.Column(db.TEXT, unique=False, nullable=True)
    spotify_id = db.Column(db.String, unique=False, nullable=True)

    albums = db.relationship('Album', backref='artist', lazy=True)
    genres = db.relationship('Genre', backref='artist', secondary=artist_genre)


class Similar(db.Model):
    __tablename__ = 'similar_artist'

    artist1_id = db.Column(UUID(as_uuid=True), db.ForeignKey("artist.id"), primary_key=True,
                           default=uuid.uuid4, unique=False, nullable=False)
    artist2_id = db.Column(UUID(as_uuid=True), db.ForeignKey("artist.id"), primary_key=True,
                           default=uuid.uuid4, unique=False, nullable=False)
    match = db.Column(db.INTEGER, unique=False, nullable=False)


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)


class Album(db.Model):
    __tablename__ = 'album'

    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    artist_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'artist.id'), default=uuid.uuid4, unique=False, nullable=False)
    image_url = db.Column(db.String, unique=False, nullable=True)
    release_date = db.Column(db.String, unique=False, nullable=True)
    mb_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4,
                      unique=True, nullable=True)
    spotify_id = db.Column(db.String, unique=False, nullable=True)


if __name__ == '__main__':
    manager.run()
