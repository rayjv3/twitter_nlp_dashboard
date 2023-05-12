
""" Twitter scraper collects tweets from provided key words
    modified from https://github.com/MartinKBeck/TwitterScraper/tree/master/snscrape/ """

import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date


def scrape(key, start=None, end=None, n=500):
    """ scrapes n number of tweets mentioning key and returns df including date/time of tweet,
    tweet id, tweet content, and username
    key (str): the keyword tweets should mention
    n (int): the number of tweets to collect (default 500)
    start (str): start date to begin looking at (YYYY-MM-DD)
    end (str): end date to stop looking at (YYYY-MM-DD) """

    #

    if start == None:
        start = "2023-01-01"
    if end == None:
        end = date.today()

    # Creating list to append tweet data to
    tweets_list = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper('{key} since:{start} until:{end}'.format(key=key, start=start, end=end)).get_items()):
        if i > n:
            break
        else:
            if tweet.lang == 'en':
                tweets_list.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username])

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

    return tweets_df

