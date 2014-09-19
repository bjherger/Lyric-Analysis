# idGrabber.py
# (C) Brendan J. Herger
# Analytics Master's Candidate at University of San Francisco
# 13herger@gmail.com
#
# Available under MIT License
# http://opensource.org/licenses/MIT
#
# *********************************
import bs4
import time

__author__ = 'bjherger'

# imports
# ###########################################

# mine
import bhUtilities

#others
import urllib2

import urlparse


#import setup
# random.seed(0)  #for consistency. Remove this if you're interested in acutal testing

# variables
############################################

# functions
############################################


def gen_search_url(artist, title, delim="+"):
    service = "http://www.lyricsmode.com/search.php?search="
    artist = delim.join(artist.split())
    title = delim.join(title.split())
    search_term = delim.join([artist, title])
    url = delim.join([service, search_term])
    return url + "&fulltext=Search&ns0=1&ns220=1#"


def get_soup(url):
    url_file = urllib2.urlopen(url).read()
    return bs4.BeautifulSoup(url_file)


def get_lyrics_url(artist, title):
    to_return = None
    search_url = gen_search_url(artist, title)
    soup = get_soup(search_url)
    table = soup.find("table", class_="songs_list")
    first_result = ""
    if table != None:
        table = table.find("a", class_ = "b search_highlight")
        first_result = table["href"]
        first_result = urlparse.urljoin(search_url, first_result)
    return first_result

def get_lyrics(artist, title):
    # time.sleep(random.uniform(0, 1))
    lyrics_url = get_lyrics_url(artist, title)
    soup = get_soup(lyrics_url)
    lyrics = soup.find("p", class_="ui-annotatable")
    lyrics = lyrics.text
    return lyrics

#main
############################################

if __name__ == "__main__":
    print "Begin Main"
    # print get_lyrics()
    print get_lyrics("lady gaga", "Just Dance")
    print "End Main"


