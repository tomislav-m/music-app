import pylast

API_KEY = "33b5d6a111174360c909fd901c387f4f"
API_SECRET = "cc5d7bc36e64f69551cae4dfdcd3f973"

network = pylast.LastFMNetwork(API_KEY, API_SECRET)


def get_library(username):
    return pylast.Library(username, network)


def get_artist(name):
    return pylast.Artist(name, network)
