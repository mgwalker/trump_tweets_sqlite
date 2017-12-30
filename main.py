import os
import urllib.request
import zipfile
import sqlite3
import datetime
from dateutil.parser import parse
import calendar
import jsonstream.reader as jsonReader

years = [2017,2016,2015,2014,2013,2012,2011,2010,2009]
year = 2017

urllib.request.urlretrieve("https://github.com/bpb27/trump_tweet_data_archive/raw/master/condensed_{}.json.zip".format(year), "tweets_{}.zip".format(year))

with zipfile.ZipFile("tweets_{}.zip".format(year),"r") as zip_ref:
    zip_ref.extractall("tweets")

def get_creation_date(tweet):
    return calendar.timegm(parse(tweet["created_at"]).timetuple())

def insert_tweet_into_db(tweet, cursor):
    cursor.execute("INSERT OR REPLACE INTO Tweets (id_str, created_at, created, text, source, retweet_count, favorite_count, is_retweet, in_reply_to_user_id_str) VALUES (?,?,?,?,?,?,?,?,?)",
        (
            tweet["id_str"],
            tweet["created_at"],
            get_creation_date(tweet),
            tweet["text"],
            tweet["source"],
            tweet["retweet_count"],
            tweet["favorite_count"],
            (1 if tweet["is_retweet"] else 0),
            tweet["in_reply_to_user_id_str"]
        )
    )

def get_tweet_count_for_year(year):
    yearConn = sqlite3.connect("databases/{}-condensed.sqlite".format(year))
    yearDB = yearConn.cursor()
    yearDB.execute("SELECT COUNT(*) FROM Tweets")
    count = yearDB.fetchone()[0]
    yearConn.close()
    return count

def get_summary_string(years):
    totalTweets = 0
    summaryString = "# Last updated on {:%B %d, %Y at %H:%M}".format(datetime.datetime.now())
    summaryString += "\n\n|Year|Tweets|\n|---|---|"
    for year in years:
        tweetCount = get_tweet_count_for_year(year)
        summaryString += "\n|{}|{:,}|".format(year, tweetCount)
        totalTweets += tweetCount
    summaryString += "\n|**Total**|**{:,}**|".format(totalTweets)
    return summaryString

def add_summary_to_readme(summaryString):
    templateFile = open("README-template", "r")
    template = templateFile.read()
    readme = open("README.md", "w")
    readme.write(template.replace("{{update}}", summaryString))
    templateFile.close()
    readme.close()

everythingConn = sqlite3.connect("databases/all-condensed.sqlite");
everythingDB = everythingConn.cursor()
everythingDB.execute("CREATE TABLE IF NOT EXISTS Tweets (id_str TEXT PRIMARY KEY, created_at TEXT, created INTEGER, text TEXT, source TEXT, retweet_count INTEGER, favorite_count INTEGER, is_retweet INTEGER, in_reply_to_user_id_str TEXT)")

specificYearConn = sqlite3.connect("databases/{}-condensed.sqlite".format(year))
specificYearDB = specificYearConn.cursor()
specificYearDB.execute("CREATE TABLE IF NOT EXISTS Tweets (id_str TEXT PRIMARY KEY, created_at TEXT, created INTEGER, text TEXT, source TEXT, retweet_count INTEGER, favorite_count INTEGER, is_retweet INTEGER, in_reply_to_user_id_str TEXT)")

stream = jsonReader.stream("tweets/condensed_{}.json".format(year))

tweet = stream.nextObject()
while tweet != False:
    insert_tweet_into_db(tweet, specificYearDB)
    insert_tweet_into_db(tweet, everythingDB)
    tweet = stream.nextObject()

summaryString = get_summary_string(years)
add_summary_to_readme(summaryString)

everythingConn.commit()
everythingConn.close()
specificYearConn.commit()
specificYearConn.close()

os.remove("tweets/condensed_{}.json".format(year))
os.rmdir("tweets")
os.remove("tweets_{}.zip".format(year))
