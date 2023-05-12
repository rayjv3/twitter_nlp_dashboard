""" contains functions for generating figures """

import matplotlib.pyplot as plt
import plotly.graph_objects as go
from textblob import TextBlob
import numpy as np
import pandas as pd

class dfMissingCol(Exception):

    def __init__(self, msg = ""):
        self.msg = msg

    def __str__(self):
        return self.msg + "Please ensure dataframe was created using scraper library"

def analyze_sentiment(tweets, sorted=False):
    """ performs sentiment analysis on  given dataframe and returns df with added sentiments column
    tweets (df): dataframe from twitter scraper
    sorted (bool): determine if tweets will be sorted by sentiment value
    returns: tweets (df) with new sentiments column """

    if not isinstance(tweets, pd.DataFrame):
        raise TypeError("Please ensure argument is a pandas dataframe")

    # create dictionary with sentiments of lyrics
    sentiments = []

    try:
        for tweet in tweets.Text:
            blob = TextBlob(tweet)
            sentiments.append(blob.sentiment.polarity)

        # add sentiment list as column in df
        tweets['sentiments'] = sentiments
        x = tweets.loc[:, 'sentiments']
        # set colors for positive and negative sentiments
        tweets['Colors'] = ['red' if x < 0 else 'green' for x in tweets['sentiments']]
        if sorted is True:
            # sort by sentiment value and reassign indices
            tweets.sort_values('sentiments', inplace=True)
            tweets.reset_index(inplace=True)

        return tweets

    except AttributeError:
        raise dfMissingCol


def sentiment_analysis(tweets, topic):
    """ Performs sentiment analysis on each song
    document and plots them all in one figure
    tweets (df): column of tweet contents
    topic (str): topic of sentiment analysis"""

    # perform analysis
    tweets = analyze_sentiment(tweets, sorted=True)

    # display figure
    plt.figure(figsize=(14, 14), dpi=80)
    plt.hlines(y=tweets.index, xmin=0, xmax=tweets.sentiments)
    for x, y, tex in zip(tweets.sentiments, tweets.index, tweets.sentiments):
        t = plt.text(x, y, round(tex, 2), horizontalalignment='right' if x < 0 else 'left',
                     verticalalignment='center', fontdict={'color': 'red' if x < 0 else 'green', 'size': 10})

    # format figure
    plt.yticks(tweets.index, tweets["Username"], fontsize=8)
    plt.title('Sentiment Analysis of Tweets Mentioning {topic} in 2023'.format(topic=topic), fontdict={'size': 20})
    plt.grid(linestyle='--', alpha=0.5)
    plt.xlim(-1, 1)
    plt.xlabel("Sentiment")
    plt.tight_layout()
    plt.show()


def create_scatter(tweets, topic):
    """ Performs sentiment analysis on each song
    document and plots them all in one figure
    tweets (df): column of tweet contents
    topic (str): topic of sentiment analysis"""

    # perform analysis
    tweets = analyze_sentiment(tweets)

    # display figure
    plt.figure(figsize=(14, 14), dpi=80)
    x = list(range(len(tweets.sentiments)))
    y = tweets.sentiments
    col = np.where(y < 0, 'r', np.where(y > 0, 'g', 'k'))
    plt.scatter(x, y, c=col, s=8)

    # format figure
    plt.title('Sentiment Analysis of Tweets Mentioning {topic} in 2023'.format(topic=topic), fontdict={'size': 20})
    plt.grid(linestyle='--', alpha=0.5)
    plt.xlabel('Tweets')
    plt.ylabel('Sentiment')
    plt.tight_layout()
    plt.show()

def create_hist(tweets, topic):
    """
    produces histogram with distribution of sentiments
    tweets (df): df of tweet content
    topic (str): topic of sentiment analysis
    """

    # perform analysis
    tweets = analyze_sentiment(tweets)

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", x = tweets["sentiments"]))
    fig.update_layout(title_text=f"Distribution of Sentiment Scores for Tweets about {topic}",xaxis_title="Sentiment Score",
                      yaxis_title="Count")

    return fig

def create_pie(tweets, topic):
    """ produces pie chart representing sentiment distribution
    tweets (df): df of tweet content
    topic (str): topic of sentiment analysis """

    # perform analysis
    tweets = analyze_sentiment(tweets)

    # initialize categories
    negative = []
    neutral = []
    positive = []
    # sort sentiments
    for value in tweets.sentiments:
        if value < 0:
            negative.append(value)
        if value > 0:
            positive.append(value)
        else:
            neutral.append(value)

    # create pie chart
    sentiment = [len(negative), len(neutral), len(positive)]
    # colors
    palette = ['red', 'grey', 'green']

    trace = go.Pie(labels=['Negative', 'Neutral', 'Positive'], values=sentiment,
                   marker_colors=palette)
    data = [trace]
    fig = go.Figure(data=data)
    fig.update_layout(title_text = f"Pie Chart of Sentiments for Tweets about {topic}")

    return fig

