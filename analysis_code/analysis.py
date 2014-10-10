# MusicXMatch.py
# (C) Layla Martin
# Analytics Master's Candidate at University of San Francisco
# layla.d.martin@gmail.com
#
# Available under MIT License
# http://opensource.org/licenses/MIT
#
# *********************************
import csv
import sys
import collections

__author__ = 'lmartin'

# imports
# ###########################################
import pandas as pd
import numpy as np

import bhUtilities

# variables
# ###########################################



# functions
# ###########################################

def count_nones(df, column):
    df = pd.DataFrame(df)
    null = df[[column]].isnull().sum()
    notNull = df[[column]].notnull().sum()

    null = float(null[column])
    notNull = float(notNull[column])
    return null / (null + notNull)

def subset_years(df, low_year=1958, high_year = 2016):
    df = pd.DataFrame(df)
    df = df[df["year"] >=low_year]
    df = df[df["year"] <high_year]
    return df

def lyrics_by_years(df):
    # df["has_lyrics"] = df["lyrics_body"]
    # df["has_lyrics"] = df["has_lyrics"].apply(lambda lyrics : 1 if type(lyrics) != float else 0)

    print df["has_lyrics"]
    subset = df.loc[:, ["has_lyrics", "year"]]
    grouped = subset.groupby("year").mean()

    year, perc = zip(*grouped.to_records())
    print year
    bhUtilities.plot_x_y(year, perc)

def years_hist(df, column):
    bhUtilities.plot_hist(df[column])

def clean_df(df):
    # remove rows
    df = df[pd.notnull(df['artist'])]
    df = df[pd.notnull(df['song'])]

    # add new columns
    # has lyrics or not
    df["has_lyrics"] = df["lyrics_body"]
    df["has_lyrics"] = df["has_lyrics"].apply(lambda lyrics: 1 if type(lyrics) == str else 0)

    # number of characters
    df["lyrics_num_char"] = df["lyrics_body"]
    df["lyrics_num_char"] = df["lyrics_num_char"].apply(lambda lyrics: len(lyrics) if type(lyrics) == str else np.nan)

    # number of words
    df["lyrics_num_words"] = df["lyrics_body"]
    df["lyrics_num_words"] = df["lyrics_num_words"].apply(lambda lyrics: len(lyrics.split()) if type(lyrics) == str else np.nan)

    # number of lines
    df["lyrics_num_lines"] = df["lyrics_body"]
    df["lyrics_num_lines"] = df["lyrics_num_lines"].apply(lambda lyrics: len(lyrics.split("\n")) if type(lyrics) == str else np.nan)

    # most common word
    df["lyrics_most_common_words"] = df["lyrics_body"]
    df["lyrics_most_common_words"] = df["lyrics_most_common_words"].apply(lambda lyrics: zip(*collections.Counter(lyrics.split()).most_common())[0] if type(lyrics) == str else np.nan)

    # average word length in chars
    df["lyrics_avg_word_len_in_chars"] = df["lyrics_num_char"] / df["lyrics_num_words"]

    # average line length
    df["lyrics_avg_line_len_in_chars"] = df["lyrics_num_char"] / df["lyrics_num_lines"]

    # average line length
    df["lyrics_avg_line_len_in_words"] = df["lyrics_num_words"] / df["lyrics_num_lines"]

    # print df[["lyrics_num_char", "lyrics_num_words", "lyrics_num_lines", "lyrics_most_common_words", "lyrics_avg_word_len_in_chars", "lyrics_avg_line_len_in_chars", "lyrics_avg_line_len_in_words"]]
    # sys.exit()
    return df


def main():
    df = pd.read_csv("../data/output/total.csv")

    # remove rows with no column or no song
    df = clean_df(df)


    # print df
    print df.columns.values.tolist()

    print "\nentire database"
    print "songs not found: ", count_nones(df, "song")
    print "artists not found: ", count_nones(df, "artist")
    print "lyrics not found: ", count_nones(df, "lyrics_body")

    # df = subset_years(df, 1980, 1990)

    print "\nsubset database"
    print "songs not found: ", count_nones(df, "song")
    print "artists not found: ", count_nones(df, "artist")
    print "lyrics not found: ", count_nones(df, "lyrics_body")

    # lyrics_by_years(df)

    # years_hist(df, "lyrics_len")

    # years_hist(df, "year")

    df.to_csv("with_word_stats.csv", quoting= csv.QUOTE_ALL)
    # print df

# generate_df
# ###########################################
if __name__ == "__main__":
    print "Begin Main"
    main()
    print "End Main"

    
    