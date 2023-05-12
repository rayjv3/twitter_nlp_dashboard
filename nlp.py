import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

stop_words = set(stopwords.words('english') + stopwords.words('spanish'))

def clean_tweets(tweets):
    """
    Parses tweet to remove unecessary noise such as stop words and capitalization

    args:
        tweets (pd.DataFrame): dateframe of tweet data
    """

    tweets["Raw Text"] = tweets["Text"]

    tweet_text = tweets["Text"].to_list()

    stopwords_in = []
    filtered_tweets = []
    for t in tweet_text:

        t = re.sub(r'[^\w\s]', '', t)
        stopwords_in.append(t)

        t = t.lower()

        word_tokens = word_tokenize(t)

        t = " ".join([w for w in word_tokens if w not in stop_words])
        filtered_tweets.append(t)

    tweets["Text"] = filtered_tweets
    tweets["stopwords_in"] = stopwords_in

    return tweets