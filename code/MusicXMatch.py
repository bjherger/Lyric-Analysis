# MusicXMatch.py
# (C) Brendan J. Herger
# Analytics Master's Candidate at University of San Francisco
# 13herger@gmail.com
#
# Available under MIT License
# http://opensource.org/licenses/MIT
#
# *********************************
__author__ = 'bjherger'

# imports
# ###########################################
import bhUtilities
import json
import time
import urllib

from pprint import pprint

# variables
# ###########################################
API_BASE = "http://api.musixmatch.com/ws/1.1/"
API_KEY = None

# functions
# ###########################################


def load_API_KEY():
    """
    Loads the API Key from a text file. API Key can also be hard coded as a global variable.
    :return: API_KEY
    """
    global API_KEY
    # TODO put somewhere else
    try:
        API_KEY = bhUtilities.read_file("/private/tmp/lyrics/musicxmatch.txt")
    except:
        print "Error loading API Key. Please place API key in /private/tmp/lyrics/musicxmatch.txt, or hard code in."

    return API_KEY


def get_track_id(artist="", track=""):
    """
    Generates track track_id for given artist and track. The first matching track track_id is returned.
    :param artist: artist to search for
    :param track: track to search for
    :return: first matching track track_id, or none
    :rtype: str
    """
    # variables
    API_method = "TRACK.SEARCH?"
    delim = "+"
    query_params = dict()

    # parameters
    query_params["q_artist"] = delim.join(artist.split())
    query_params["q_track"] = delim.join(track.split())
    query_params["page_size"] = str(1)
    query_params["apikey"] = API_KEY

    query_string = urllib.urlencode(query_params)

    # generate url
    url = API_BASE + API_method + query_string

    # get page
    page = bhUtilities.read_url(url)

    # get track track_id
    track_id = bhUtilities.re_match(r"\"track_id\":([0-9]+),", page)

    if track_id:
        track_id = track_id[0]
    return track_id


def get_lyrics(artist="", track=""):
    """
    Get lyrics to the given track, by the given artist.
    :param artist: artist to search for
    :param track: track to search for
    :return: dictionary containing lyrics, and other information
    :rtype: dict
    """

    # variables
    return_dic = dict()

    # get track id
    track_id = get_track_id(artist, track)

    # no song case
    if not track_id:
        return_dic["lyrics_body"] = None

    # song found case
    else:

        # generate query

        query_params = dict()
        query_params["apikey"] = API_KEY
        query_params["track_id"] = track_id

        query_string = urllib.urlencode(query_params)

        # generate url
        url = "http://api.musixmatch.com/ws/1.1/track.lyrics.get?" + query_string

        # get page
        json_raw = bhUtilities.read_url(url)

        # get JSON
        data = json.loads(json_raw)
        # lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
        # pprint(data["message"]["body"]["lyrics"].keys())

        # update return dict with lyric content.
        return_dic = data["message"]["body"]["lyrics"]
        return_dic.update(data["message"]["header"])

    return_dic["retrieval_time"] = time.asctime(time.gmtime())

    # add lyrics_ to all keys
    for (key, value) in return_dic.items():
        key = str(key)
        if not key.startswith("lyrics_"):
            new_key = "lyrics_" + key
            return_dic[new_key] = return_dic.pop(key)

    return return_dic


# main
# ###########################################
load_API_KEY()
if __name__ == "__main__":
    # TODO reuire has _lyrics key
    print get_track_id("2 chainz", "no lie")
    pprint(get_lyrics("2 chainz", "no lie"))
    # pprint(get_lyrics("lady gaga", "bad romance"))

