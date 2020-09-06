import pylast

API_KEY = ""
API_SECRET = ""

network = pylast.LastFMNetwork(API_KEY, API_SECRET)


def get_library(username):
    return pylast.Library(username, network)


def get_artist(name):
    return pylast.Artist(name, network)
