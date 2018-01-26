# Trump tweets in SQLite

Takes the JSON data harvested by [trump_tweet_data_archive](https://github.com/bpb27/trump_tweet_data_archive)
and makes it available as SQLite databases.  Updates every 6 hours.

# Last updated on January 26, 2018 at 10:00

|Year|Tweets|
|---|---|
|2018|192|
|2017|2,605|
|2016|4,225|
|2015|7,536|
|2014|5,784|
|2013|8,144|
|2012|3,531|
|2011|774|
|2010|142|
|2009|56|
|**Total**|**32,989**|

## Data

The databases are located in the [databases](databases/) directory.  They are split by year, but
there is one database that has everything together.

* [everything](databases/all-condensed.sqlite)
* [2009](databases/2009-condensed.sqlite)
* [2010](databases/2010-condensed.sqlite)
* [2011](databases/2011-condensed.sqlite)
* [2012](databases/2012-condensed.sqlite)
* [2013](databases/2013-condensed.sqlite)
* [2014](databases/2014-condensed.sqlite)
* [2015](databases/2015-condensed.sqlite)
* [2016](databases/2016-condensed.sqlite)
* [2017](databases/2017-condensed.sqlite)

## Schema

All of the tweets are rows in a table called
`Tweets` - its structure is lifted directly from the structure of the JSON files at the source, but
with an added `created` column, which is the Unix epoch timestamp.

|column|type|description|
|---|---|---|
|id_str|TEXT|**PRIMARY KEY** Tweet ID as a string
|created_at|TEXT|Text version of the creation date
|created|INTEGER|Creation date as a Unix epoch timestamp
|text|TEXT|The text of the tweet
|source|TEXT|Twitter client (e.g., "Twitter for iPhone", "Twitter Web Client", etc.)
|retweet_count|INTEGER|How many times it was retweeted
|favorite_count|INTEGER|How many times it was favorited
|is_retweet|INTEGER|Whether or not the tweet is a retweet, the "new" way.  Does not include manual retweets
|in_reply_to_user_id_str|TEXT|If the tweet is a reply to someone, their user ID as a string
