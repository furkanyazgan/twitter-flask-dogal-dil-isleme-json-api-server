from flask import  Flask ,jsonify ,request




import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import re
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from os import kill, write

from cleantext import clean

auth = tweepy.OAuthHandler("*****************", )
auth.set_access_token("**********", "************")
api = tweepy.API(auth)



def tweet_revize(temp):


    while (temp.count("http") != 0 ):
        # print("ÇALIŞTI: "+temp.count("http"))

        index = temp.find("http")
        temp = temp[:index] + temp[index + 23:]

    return clean(temp, no_emoji=True)


def convert_map(tweet, analysis, score):
    temp_map = {}
    temp_map["tweet"] = tweet
    temp_map["polarity"] = analysis.sentiment.polarity
    temp_map["subjectivity"] = analysis.sentiment.subjectivity
    temp_map["negatif"] = score["neg"]
    temp_map["notr"] = score["neu"]
    temp_map["pozitif"] = score["pos"]
    return temp_map








def get_tweets(hashtag):
    keyword = "#" + str(hashtag)
    noOfTweet = 100


    tweet_map_list = []

    for tweet_info in tweepy.Cursor(api.search_tweets, q=keyword, lang='en', tweet_mode='extended').items(noOfTweet):
        if 'retweeted_status' in dir(tweet_info):
            tweet = tweet_info.retweeted_status.full_text
        else:
            tweet = tweet_info.full_text

        revize_tweet = tweet_revize(str(tweet))

        analysis = TextBlob(revize_tweet)
        score = SentimentIntensityAnalyzer().polarity_scores(revize_tweet)

        temp_map = convert_map(revize_tweet,analysis,score)

        if(temp_map in tweet_map_list):
            pass
        else:
            tweet_map_list.append(temp_map)


    return tweet_map_list







app= Flask(__name__)

@app.route("/")
def baslangic():
    hashtag = request.args.get("hashtag")

    temp = get_tweets(hashtag)
    print(temp)

    return jsonify(miktar= len(temp),tweets=temp)

if __name__ ==  "__main__":
    app.run()
