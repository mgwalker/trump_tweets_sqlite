import os
import urllib.request
import zipfile
import sqlite3
from dateutil.parser import parse
import calendar
import jsonstream.reader as jsonReader

year = 2017

urllib.request.urlretrieve("https://github.com/bpb27/trump_tweet_data_archive/raw/master/condensed_{}.json.zip".format(year), "tweets_{}.zip".format(year))

with zipfile.ZipFile("tweets_{}.zip".format(year),"r") as zip_ref:
    zip_ref.extractall("tweets")

def get_creation_date(tweet):
    return calendar.timegm(parse(tweet["created_at"]).timetuple())

def insert_tweet_into_db(tweet, cursor):
    cursor.execute("INSERT OR IGNORE INTO Tweets (id_str, created_at, created, text, source, retweet_count, favorite_count, is_retweet, in_reply_to_user_id_str) VALUES (?,?,?,?,?,?,?,?,?)",
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

conn = sqlite3.connect("{}-condensed.sqlite".format(year))
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Tweets (id_str TEXT PRIMARY KEY, created_at TEXT, created INTEGER, text TEXT, source TEXT, retweet_count INTEGER, favorite_count INTEGER, is_retweet INTEGER, in_reply_to_user_id_str TEXT)")

stream = jsonReader.stream("tweets/condensed_{}.json".format(year))

tweet = stream.nextObject()
count = 0
while tweet != False:
    count += 1
    insert_tweet_into_db(tweet, cursor)
    tweet = stream.nextObject()
conn.commit()
conn.close()

os.remove("tweets/condensed_{}.json".format(year))
os.rmdir("tweets")
os.remove("tweets_{}.zip".format(year))
