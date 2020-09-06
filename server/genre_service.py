from database import Genre, db


def get_genre(genre):
    return Genre.query.filter_by(name=genre).first()


def insert_genre(genre):
    db.session.add(genre)
    db.session.commit()


def insert_artist_genre(artist_genre):
    db.session.add(artist_genre)
    db.session.commit()
