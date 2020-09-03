from database import Album, db
from typing import List


def get_album(album):
    return Album.query.filter_by(name=album).first()


def get_albums() -> List[Album]:
    return Album.query.all()


def get_album_spotify(spotify_id):
    return Album.query.filter_by(spotify_id=spotify_id).first()


def insert_album(album):
    db.session.add(album)
    db.session.commit()
