# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:40:31 2014

@author: laylamartin
"""
# TODO add '__author__ = ' tag

# TODO organize imports alphabetically

from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import re


def get_billboard_pages():
    """
    DESCRIPTION: scrapes raw html data from the billboard's hot-100
    PARAMS: none
    RETURNS: globalPageList: a list where each entry is a dictionary with one 
     key-value pair. The key is the year and the value is the raw data from 
     that years billboard hot-100 archive.
    """
    globalPageList = []
    year_list = []
    
    #TODO remove this for loop.
    for i in range(1958,2015):
        year_list.append(i)
    # scrape web of billboard archives 'hot 100' pages from year 1960 to 2014:

    # TODO change to for year in range ....
    for year in year_list:
        url = "http://www.billboard.com/archive/charts/" + str(year) + "/hot-100"

        # TODO put request in try, catch
        request = urllib2.Request(url)
        print 'Querying', url
    
        try:
            page = urllib2.urlopen(request)

        # TODO change to Exception, e
        except urllib2.URLError, e:
            print "ERROR with year", year
            if hasattr(e, 'reason'):
                print 'Failed to reach url'
                print 'Reason: ', e.reason
                #sys.exit()
            elif hasattr(e, 'code'):
                if e.code == 404:
                    print 'Error: ', e.code
                    #sys.exit()

        #  TODO put in try block
        soup = BeautifulSoup(page) #  TODO put in try block
        soup = soup.prettify() #  TODO put in try block
        soup = str(soup) #  TODO put in try block

        # TODO add url to localYearDic
        # TODO dict should have keys ["year", "soup", "url"]
        # TODO if you're using this format for DataFrame compatability, specify that.
        localYearDic = {year:soup}
        globalPageList.append(localYearDic)
        
    return globalPageList



# TODO this funciton is unnecessary. program should read from web, and act on data directly.
# TODO it is too expensive / risky to save .html to file in this way
def write_hot_files(dic_list = get_billboard_pages()):
    # TODO don't call to get_billboard_soup() as a parameter. remove the parameter and just call to
    # TODO get_billboard_soup() in the body of the funciton
    """
    DESCRIPTION: parses the list of html billboard hot 100 pages and writes
     each as a separate file.
    PARAMS: allBillboardData: list of dictionaries generated from function
     get_billboard_soup().
    RETURNS: nothing, writes each html as a file in the working directory
    """

    # TODO change to: for xxx in dic_list.values()
    for i in range(len(dic_list)):

        # TODO change to: for sub_dict in dict_list.values()
        for key in dic_list[i]:
            year = key
            bs4_text = dic_list[i][key]
            #html_str = bs4_text 
            file_name = "billboard_hot_" + str(year)
            # TODO rename html_file. this suggests that the file is a .html
            Html_file= open(file_name,"w")
            try:
                Html_file.write(bs4_text)
            except:
                print "Unable to write to file. Check if type is string."
            # TODO use try/except/finally, put Html_file.close() in finally
            Html_file.close()

            

        
       
def make_chart(year_list):
    """
    DESCRIPTION: writes all billboard data for specified years into a data frame
     and writes this to a csv in working directory. Possible errors encountered 
     are printed and should help identify if/which format was unreadable.
    PARAMS: year_list: a list of desired years to write to the data frame.
    RETURNS: nothing, optional to return the data frame.
    """
    for year in year_list:
                
        num_errors = 0
        # TODO html file directly. It is too expensive to read from web, write to disk, and then read from disk.
        file_name = "billboard_hot_" + str(year)
        html_text = open(file_name,"r")
        raw_text = html_text.read()
        
        soup = BeautifulSoup(raw_text)

        # get all soup having to do with rows of the table:
        # TODO rename rows, too generic. perhaps week / entry
        rows = soup.find("table").find("tbody").find_all("tr")

        # initialize empty list to hold weekly entries for one year:
        week_entry = []
        
        # range through rows (weeks) of the billboard chart and get info:
        # TODO for entry in rows:
        for i in range(len(rows)):
            row = rows[i]
            entry_lst = row.find_all('td')
            # TODO write comment describing why two cases are necessary
            if len(entry_lst) == 3:
                #print entry_lst
                date_loc = entry_lst[0]
                song_loc = entry_lst[1]
                artist_loc = entry_lst[2]
            # TODO else if
            if len(entry_lst) == 1:
                #print entry_lst
                date_loc = entry_lst[0]
            # TODO else
            if len(entry_lst) != 1 and len(entry_lst) != 3:
                print "ERROR: unexpected format in row for year", year
                print "Advise: check format for this year."
            
            # parse html to obtain shortest string of info per category:

            # TODO combine these 5 try excepts into 1. perhaps use .get or a default value
            # TODO it is not necessary to have this level of detail in errors
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
            #  as song titles because they will be in this format instead.
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
            # TODO depending on desired output, this might work. If it were going to csv, it would be fine.
            # TODO however, because we are converting to Pandas, just convert string to a date object
            match_date = re.match(r'.*\/(\d{4}-\d{2}-\d{2})\/.*', raw_date)
            # check if date is in valid format, otherwise, use None:
            try:
                date = match_date.group(1)
            except:
                print "Error with MATCHING date:", match_date
                num_errors += 1
                date = None
            
            # extract song title:
            # TODO write funciton to process string. should be lower case, stripped, and have non-alpha-numierc
            # TODO characters removed
            song = raw_song.strip().lower()
                
            # extract song title:
            # TODO write funciton to process string. should be lower case, stripped, and have non-alpha-numierc
            # TODO characters removed
            artist = raw_artist.strip().lower()
            
            # create dictionary per week:
            # TODO include unique identifier, url, page title, scraped timestamp
            entry_dic = {"year":year, "date":date, "song":song, "artist":artist}
            week_entry.append(entry_dic)
        
        # print to data frame  :  
        yearly_df = pd.DataFrame(week_entry)
        
        # sort df columns by date (unneeded i think):
        #yearly_df = yearly_df.sort(columns = ["date"])
        
        try:
            # TODO This doesn't seem to make sense. create one long list of dictionaries, then convert that to a dataframe
            all_years_df = all_years_df.append(yearly_df, ignore_index = True)
        except:
            all_years_df = yearly_df
            print "Data Frame Initiated"
                        
            
    print "TOTAL ERRORS:", num_errors
    all_years_df.to_csv('BILLBOARD_HOT_100.csv')

    # TODO uncomment return
    #return all_years_df
        
        
#  TODO rename to main()
def do_the_whole_thing():
    """
    scrape the site, save the internet data as files, read the files back in
    and output them as an aggregated data frame. done.
    """
    # scrape the website for all the info:
    # TODO use_underscores instead of camelCase
    globalPageList = get_billboard_pages()
    
    # write each year as an out_file in the working directory:
    # not necessary
    write_hot_files(globalPageList)
    
    # specify years to use:
    # data is for years 1958 to 2014:
    # TODO remove this. put logic in a function
    year_list = []
    for i in range(1958,2015):
        year_list.append(i)

    # write the final data frame, saved as a csv:
    # TODO make creating dataframe, writing dataframe two separate funciton calls
    make_chart(year_list) 
    
    
    
    
    
       
       