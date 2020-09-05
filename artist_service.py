from database import Artist, Similar, db
from typing import List

PAGE_SIZE = 100


def get_artist(name) -> Artist:
    artist = Artist.query.filter_by(name=name).first()
    return artist


def get_all_artists() -> List[Artist]:
    return Artist.query.all()


def get_artists(page: int = 1, page_size: int = PAGE_SIZE) -> List[Artist]:
    return Artist.query.limit(page_size).offset((page-1)*PAGE_SIZE)


def save_artist():
    db.session.commit()


def artist_exist(name):
    return (get_artist(name) is not None)


def insert_artists(artists):
    db.session.add_all(artists)
    db.session.commit()


def insert_artist(artist):
    db.session.add(artist)
    db.session.commit()


def insert_similar(similar):
    db.session.add(similar)
    db.session.commit()


def get_similar(id1, id2):
    return Similar.query.filter_by(artist1_id=id1, artist2_id=id2).first()


def get_all_similar() -> [Similar]:
    return Similar.query.all()
