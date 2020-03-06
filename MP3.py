import win_unicode_console # Apparently fixes encoding errors
win_unicode_console.enable()

import twitter
from config import *

api = twitter.Api(consumer_key=API_key,
                  consumer_secret=API_secret_key,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)

timeline = api.GetUserTimeline(screen_name="zachary3352", include_rts=0, count=100)
user = api.GetUser(screen_name="zachary3352")

all_tweets = open("alltweets.txt", "w+")

def convert_to_utf8(list):
    for item in list:
        item.text.encode('utf8')

for tweet in timeline:
    all_tweets.write(str(tweet.text))
    all_tweets.write("\n")

print("You've liked", user.favourites_count, "tweets.")

def ignore_retweets(tweet): # Got this idea from https://gist.github.com/codeinthehole/0e7430d79f3dcd1235c89f9367a49a1b
    if not tweet.text.startswith("RT"):
        return tweet
