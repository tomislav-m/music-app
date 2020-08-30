from flask import jsonify
from mylast import get_library
import mylast
from database import app, Artist, Similar
import artist_service


@app.route('/')
def hello_world():
    return jsonify('Hello')


@app.route('/artists')
def save_artists():
    library = get_library("walflower27")
    artists = library.get_artists(1000)
    artists_dict = {}
    artists_to_save = []
    i = 0
    for artist in artists:
        try:
            artist_name = artist.item.name
            if artist_service.artist_exist(artist_name):
                continue

            app.logger.info(artist_name)
            artist_model = Artist(name=artist_name, mb_id=artist.item.get_mbid(),
                                  image_url=artist.item.get_cover_image(), bio=artist.item.get_bio_content())
            artists_to_save.append(artist_model)

            artists_dict[i] = artist_name
            i += 1
        except Exception:
            continue
    artist_service.insert_artists(artists_to_save)
    return artists_dict


@app.route('/similar')
def save_similar():
    artists = artist_service.get_all_artists()
    all_similar_ids = list(
        map(lambda x: x.artist1_id, artist_service.get_all_similar()))
    for artist in reversed(artists):
        if artist.id in all_similar_ids:
            continue
        artist_last = mylast.get_artist(artist.name)
        similar_artists = artist_last.get_similar()

        for similar in similar_artists:
            try:
                artist2 = next(filter(lambda x: x.name ==
                                      similar.item.name, artists) or [], None)
                if artist2 is not None:
                    similar_db = artist_service.get_similar(
                        artist.id, artist2.id)
                    if similar_db is not None:
                        # app.logger.info(
                        #     {"artist1": artist.name, "artist2": artist2.name, "match": similar_db.match})
                        continue
                    similar_model = Similar(
                        artist1_id=artist.id, artist2_id=artist2.id, match=similar.match)
                    artist_service.insert_similar(similar_model)
                    app.logger.info(
                        {"artist1": artist.name, "artist2": artist2.name, "match": similar.match})
            except Exception:
                app.logger.info(artist.name)
                continue
    return "Done"


if __name__ == '__main__':
    app.run()
