from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from database import Artist, Album


class ArtistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
        include_relationships = True
        load_instance = True

    image_url = fields.Str(data_key='imageUrl')
    mb_id = fields.Str(data_key='mbId')
    spotify_id = fields.Str(data_key='spotifyId')


class AlbumSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Album
        include_relationships = True
        load_instance = True

    artist = fields.Pluck(ArtistSchema, field_name='name', data_key='artist')
    image_url = fields.Str(data_key='imageUrl')
    mb_id = fields.Str(data_key='mbId')
    spotify_id = fields.Str(data_key='spotifyId')
    release_date = fields.Str(data_key='releaseDate')
