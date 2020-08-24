from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
from sqlalchemy import Table
from sqlalchemy.orm import relationship

app = Flask(__name__)

DB_URL = 'postgresql://postgres:postgres@localhost:5432/Music'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

artist_genres = Table('artist_genres', db.metadata,
                      db.Column('artist_id', UUID(as_uuid=True), db.ForeignKey('artists.id')),
                      db.Column('genre_id', UUID(as_uuid=True), db.ForeignKey('genres.id')))

similar_artists = Table('similar_artists', db.metadata,
                        db.Column('artist1_id', UUID(as_uuid=True), db.ForeignKey('artists.id')),
                        db.Column('artist2_id', UUID(as_uuid=True), db.ForeignKey('artists.id')),
                        db.Column('match', db.NUMERIC, default=0))


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    image_url = db.Column(db.String, unique=False, nullable=True)
    mb_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=True)
    bio = db.Column(db.TEXT, unique=False, nullable=True)

    children = relationship("Child", secondary=artist_genres)


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)


if __name__ == '__main__':
    manager.run()
