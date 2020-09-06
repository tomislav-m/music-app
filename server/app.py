from flask import jsonify
from mylast import get_library
import mylast
from database import app, Artist, Similar, Album, Genre
import artist_service
import myspotify
import album_service
import genre_service
from schemes import ArtistSchema, AlbumSchema


@app.route('/')
def hello_world():
    return jsonify('Hello')


@app.route('/save_artists')
def save_artists():
    users = []
    artists_dict = {}
    i = 0
    for user in users:
        library = get_library(user)
        artists = library.get_artists(None)
        artists_to_save = []
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
                artist_service.insert_artist(artist_model)
                i += 1
            except Exception:
                continue
    return artists_dict


@app.route('/albums/<date>')
def get_albums(date):
    albums = album_service.get_albums_filter(
        Album.release_date.like(f'%-{date}'))
    album_schema = AlbumSchema(many=True)
    dump_data = album_schema.dump(albums)
    return jsonify(dump_data)


@app.route('/similar')
def save_similar():
    artists = artist_service.get_all_artists()
    for artist in artists:
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


@app.route('/albums')
def save_albums():
    artists = artist_service.get_artists(1, 2817)
    albums_dict = {}
    index = 0
    for artist in artists:
        try:
            albums = myspotify.sp.search(artist.name, 50, 0, "album", "US")
            for album in list(albums['albums']['items']):
                if album['album_type'] == "single" or album_service.get_album_spotify(album['id']) is not None:
                    continue
                if (album['artists'][0]['name'].lower() == artist.name.lower()):
                    album_name = album['name']
                    albums_dict[index] = album_name
                    index += 1

                    image_url = ""
                    if len(album['images']) > 0:
                        image_url = album['images'][0]['url']
                    try:
                        album_service.insert_album(Album(
                            name=album_name, artist_id=artist.id, image_url=image_url,
                            release_date=album['release_date'], mb_id=None, spotify_id=album['id']))
                    except Exception as exc:
                        app.logger.error(exc)
        except Exception as exc_out:
            app.logger.error(exc_out)
    return albums_dict


@app.route('/artists_spotify')
def save_artists_spotify():
    artists = artist_service.get_artists(1, 3000)
    genres_arr = []
    for artist in artists:
        if len(artist.genres) > 0:
            continue
        if artist.spotify_id is None:
            artists_sp = myspotify.sp.search(
                artist.name, 1, 0, "artist", market="US")['artists']['items']
            if len(artists_sp) == 0:
                continue
            artist_sp = artists_sp[0]
            artist.spotify_id = artist_sp['id']
            if len(artist_sp['images']) > 0:
                artist.image_url = artist_sp['images'][0]['url']
            genres = artist_sp['genres']
            for genre in genres:
                genre_db = genre_service.get_genre(genre)
                if genre_db is None:
                    genres_arr.append(genre)
                    genre_service.insert_genre(Genre(name=genre))
                    genre_db = genre_service.get_genre(genre)
                artist.genres.append(genre_db)
            artist_service.save_artist()
    return jsonify(genres_arr)


if __name__ == '__main__':
    app.run()
