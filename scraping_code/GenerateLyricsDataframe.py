# GenerateLyricsDataframe.py
# (C) Layla Martin
# Analytics Master's Candidate at University of San Francisco
# layla.d.martin@gmail.com
#
# Available under MIT License
# http://opensource.org/licenses/MIT
#
# *********************************
import bhUtilities

__author__ = 'lmartin'

# imports
# ###########################################
import re
import time
import urllib2

import pandas as pd
pd.set_option("max_colwidth", 3)


# specific
from bs4 import BeautifulSoup

# specific to this package
import MusicXMatch

# variables
# ###########################################

# functions
# ###########################################

def get_billboard_soup(genre, start_year=1958, end_year = 2015):
    """
    Get raw pages and some meta information for given genre and year range
    :param genre: genre to scrape, must be of the form used by billboard.com
    :param start_year: year to start search with
    :return: dictionary, of the form {year : [soup, request_time, url] }
    :rtype: dict
    """
    # variables
    year_dict = {}

    # loop through years of interest
    for year in xrange(start_year, end_year):

        # web scraping sucks, try it first
        try:

            # get url
            url = "http://www.billboard.com/archive/charts/" + str(year) + "/" + genre
            request = urllib2.Request(url)
            print 'Querying', url

            # get raw page
            page = urllib2.urlopen(request).read()
            request_time = time.time()

            # get soup
            soup = BeautifulSoup(page)
            soup = soup.prettify()

            # add to dictionary
            # TODO make it a dict
            year_dict[year] = [soup, request_time, url]

        # output infomation related to errors
        except urllib2.URLError, e:
            print "Error with year", year
            if hasattr(e, 'reason'):
                print 'Failed to reach url'
                print 'Reason: ', e.reason
                print 'No data available for', genre, 'for year', year
            elif hasattr(e, 'scraping_code'):
                if e.code == 404:
                    print 'Error: ', e.code
            continue

    return year_dict


# noinspection PyBroadException,PyUnboundLocalVariable
def scrape_single_genre(year_dict, genre):

    # variables
    results_list = []

    # loop through dict
    for (year, year_attribute_list) in year_dict.iteritems():

        print "scraping: ", year
        # variables
        num_errors = 0

        # unpack soup, meta information
        raw_text = year_attribute_list[0]
        billboard_request_time = year_attribute_list[1]
        billboard_url = year_attribute_list[2]
        soup = BeautifulSoup(raw_text)

        # get table rows
        rows = soup.find("table").find("tbody").find_all("tr")

        # range through rows (weeks) of the billboard chart and get info:
        for row in rows:

            entry_lst = row.find_all('td')

            # date, song and artist
            if len(entry_lst) == 3:
                date_loc = entry_lst[0]
                song_loc = entry_lst[1]
                artist_loc = entry_lst[2]

            # date only
            elif len(entry_lst) == 1:
                date_loc = entry_lst[0]

            # something went wrong
            elif len(entry_lst) != 1 and len(entry_lst) != 3:
                print "ERROR: unexpected format in row for year", year
                print "Advise: check format for this year."

            # Parse all possible values
            # ###############################################

            # parse html to obtain shortest string of info per category:
            try:
                raw_date = date_loc.a['href']
            except:
                print "ERROR: DATE:", row
                num_errors += 1
            try:
                raw_song = str(song_loc.contents[0])
            except:
                print "ERROR: SONG:", row
                num_errors += 1

            # some artists don't have <a> tags, so treat them in the same manner
            # as song titles because they will be in this format instead.
            if artist_loc.a is None:
                try:
                    raw_artist = str(artist_loc.contents[0])
                except:
                    print "ERROR: ARTIST:", row
                    num_errors += 1
            else:
                try:
                    raw_artist = str(artist_loc.a.contents[0])
                except:
                    print "ERROR: ARTIST:", row
                    num_errors += 1

            # extract date:
            match_date = re.match(r'.*\/(\d{4}-\d{2}-\d{2})\/.*', raw_date)

            # check if date is in valid format, otherwise, use None:
            try:
                date = match_date.group(1)
            except:
                print "Error with MATCHING date:", match_date
                num_errors += 1
                date = None

            # extract song title:
            song = raw_song.strip().lower()

            # extract song title:
            artist = raw_artist.strip().lower()

            try:
                lyrics_dic = MusicXMatch.get_lyrics(artist=artist.split(" featuring", 1)[0], track=song)
            except:
                lyrics_dic = dict()


            # add all gathered information to a dict
            song_dic = {"year": year, "date": date, "song": song,
                         "artist": artist, "genre": genre,
                         "billboard_request_time": billboard_request_time,
                         "billboard_url": billboard_url}

            # add lyrics to song_dic
            song_dic.update(lyrics_dic)

            # add song to results_list
            results_list.append(song_dic)

    print "TOTAL ERRORS:", num_errors

    return results_list


def write_csv_from_df(data_frame):
    """
    """
    csv_name = "../data/output/"+bhUtilities.time_as_string() + "billboard_temp_data.csv"
    data_frame.to_csv(csv_name, s, encoding="utf-8")


def write_csv_from_lst(row_list):
    """
    """
    csv_name = "billboard_temp_data.csv"
    data_frame = pd.DataFrame(row_list)
    data_frame.to_csv(csv_name, index=False)


def generate_df():
    total_results = []

    category_list = [
                     {'extension': 'r-b-hip-hop-songs', 'genre': 'r_and_b_hip_hop'},
                     {'extension': 'adult-contemporary', 'genre': 'adult_contemp'},
                     {'extension': 'hot-100', 'genre': 'hot_100'},
                     {'extension': 'germany-songs', 'genre': 'germany'},
                     {'extension': 'country-songs', 'genre': 'country'},
                     {'extension': 'holiday-songs', 'genre': 'holiday_airplay'},
                     {'extension': 'billboard-200', 'genre': 'billboard_200'},
                     {'extension': 'dance-club-play-songs', 'genre': 'dance_club_songs'},
                     {'extension': 'tropical-songs', 'genre': 'latin_tropical'},
                     {'extension': 'hot-mainstream-rock-tracks', 'genre': 'rock_mainstream'},
                     {'extension': 'latin-songs', 'genre': 'hot_latin'},
                     {'extension': 'alternative-songs', 'genre': 'rock_alternative'},
                     {'extension': 'rap-song', 'genre': 'rap'},
                     {'extension': 'radio-songs', 'genre': 'radio'},
                     {'extension': 'country-airplay', 'genre': 'country_airplay'},
                     {'extension': 'pop-songs', 'genre': 'pop'},
                     {'extension': 'adult-pop-songs', 'genre': 'adult_pop'},
                     {'extension': 'rhythmic-40', 'genre': 'rhythmic'},
                     {'extension': 'regional-mexican-songs', 'genre': 'regional_mexican'},
                     {'extension': 'latin-pop-songs', 'genre': 'latin_pop'}
        ,
                     {'extension': 'hot-r-and-b-hip-hop-airplay', 'genre': 'r_and_b_hip_hop_airplay'},

                     {'extension': 'digital-songs', 'genre': 'digital'},
                     {'extension': 'hot-dance-airplay', 'genre': 'dance_mix_show_airplay'},
                     {'extension': 'christian-songs', 'genre': 'hot_christian'},
                     {'extension': 'social-50', 'genre': 'social_50'},
                     {'extension': 'summer-songs', 'genre': 'summer'},
                     {'extension': 'heatseekers-songs', 'genre': 'heatseekers'},
                     {'extension': 'japan-hot-100', 'genre': 'japan_hot_100'},
                     {'extension': 'france-songs', 'genre': 'france'},
                     {'extension': 'canadian-hot-100', 'genre': 'canadian_hot_100'},
                     {'extension': 'dance-electronic-digital-songs', 'genre': 'dance_electronic_digital'},
                     {'extension': 'rock-songs', 'genre': 'hot_rock'},
                     {'extension': 'rock-digital-songs', 'genre': 'rock_digital'},
                     {'extension': 'triple-a', 'genre': 'adult_alternative'},
                     {'extension': 'jazz-songs', 'genre': 'smooth_jazz'},
                     {'extension': 'gospel-songs', 'genre': 'hot_gospel'},
                     {'extension': 'gospel-digital-songs', 'genre': 'gospel_digital'},
                     {'extension': 'christian-digital-songs', 'genre': 'christian_digital'},
                     {'extension': 'on-demand-songs', 'genre': 'on_demand'},
                     {'extension': 'streaming-songs', 'genre': 'streaming'},
                     {'extension': 'k-pop-hot-100', 'genre': 'k_pop_100'},
                     {'extension': 'united-kingdom-songs', 'genre': 'uk_singles'},
                     {'extension': 'youtube', 'genre': 'youtube'}
                 ]

    # iterate through categories, for all years
    for category in category_list[:]:

        # unpack variables
        extension = category.get('extension', None)
        genre = category.get('genre', None)

        # gen the soup and meta information for all years
        soups_to_scrape_dict = get_billboard_soup(extension)

        # scrape a list of pages
        genre_weekly_list = scrape_single_genre(soups_to_scrape_dict, genre)
        total_results.extend(genre_weekly_list)

    # convert to dataframe
    global_weekly_entry_df = pd.DataFrame(total_results)

    # output dataframe
    print global_weekly_entry_df
    write_csv_from_df(global_weekly_entry_df)

    # ... and return
    return global_weekly_entry_df

# generate_df
# ###########################################
if __name__ == "__main__":
    print "Begin Main"
    bhUtilities.timeItStart()
    df = generate_df()
    bhUtilities.timeItEnd()
    print "End Main"

    
    