from database import Album, db
from typing import List

PAGE_SIZE = 100


def get_album(album):
    return Album.query.filter_by(name=album).first()


def get_albums(page: int = 1, page_size: int = PAGE_SIZE) -> List[Album]:
    return Album.query.limit(page_size).offset((page-1)*PAGE_SIZE)


def get_albums_filter(filter):
    return Album.query.filter(filter).all()


def get_album_spotify(spotify_id):
    return Album.query.filter_by(spotify_id=spotify_id).first()


def insert_album(album):
    db.session.add(album)
    db.session.commit()
