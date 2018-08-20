import tweepy
import csv
import sqlite3


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError:
            print("error")
            break


consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

name = []
with open('list_of_ppl.txt', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count +=1
		name.append(row["name"])
		line_count+=1

# public_tweets = api.home_timeline()
# foreach through all tweets pulled
# name = "Cardinals"

conn = sqlite3.connect('tweet.db')
c = conn.cursor()
# c.execute("""CREATE TABLE tweet (
# 	unique_ID integer,
# 	tweet_ID text,
# 	tweet text,
# 	tweet_dates date,
# 	tweet_place text,
# 	retweet_count integer,
# 	followers integer,
# 	location text,
# 	friends_count integer,
# 	user_created_account date)
# 	""")



for i in name:
	counter = 0
	print("*********************"+i+"*************************")
	print("*********************"+i+"*************************")
	print("*********************"+i+"*************************")
	print("*********************"+i+"*************************")




	for status in limit_handled(tweepy.Cursor(api.user_timeline, id=i).items()):


		check = []

		unique_tweet_id = (status._json['id'])


		tweet_name = (status._json['user']['screen_name'])
		verify = (status._json['user']['verified'])

		tweet_id = (status._json['user']['name'])
		a = api.get_status(unique_tweet_id, tweet_mode='extended')
		text = a.full_text
		# text = (status._json["extended_tweet"]["full_text"])
		dates = (status._json['created_at'])
		place = (status._json['place'])
		if place != None:
			place = (status._json['place']['full_name'])

		retweet_count = (status._json['retweet_count'])
		followers = (status._json['user']['followers_count'])
		location = (status._json['user']['location'])

		friends_count = (status._json['user']['friends_count'])
		account_created = (status._json['user']['created_at'])
		check.append(unique_tweet_id)
		check.append(tweet_id)
		check.append(text)
		check.append(dates)
		check.append(place)
		check.append(retweet_count)
		check.append(followers)
		check.append(location)
		check.append(friends_count)
		check.append(account_created)
		check.append(tweet_name)
		check.append(verify)
		c.execute("INSERT INTO tweet VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (check))
		conn.commit()
	# tcount = 3200
	# results = api.user_timeline(id=i,count=tcount)
	# for tweet in results:
	# 	print(tweet.text)
		counter+=1
	print(counter)

conn.close()

