from datetime import *
import twitter
from config import *

def get_tweets(screen_name):
    api = twitter.Api(consumer_key=API_key,
                      consumer_secret=API_secret_key,
                      access_token_key=access_token,
                      access_token_secret=access_token_secret,
                      tweet_mode= 'extended')
    timeline = api.GetUserTimeline(screen_name=screen_name, include_rts=0, count=199)
    user = api.GetUser(screen_name=screen_name)

    all_tweets = open("alltweets.txt", "r+")

    print(all_tweets.readline(), "\n", date.today(), "\n", all_tweets.readline(), "\n", str(date.today()-timedelta(days=1)).split(" ")[0], "\n", all_tweets.readline(), "\n", str(date.today()-timedelta(days=2)).split(" ")[0])

    # if all_tweets.readline() == date.today() or all_tweets.readline() == str(date.today()-timedelta(days=1)).split(" ")[0] or all_tweets.readline() == str(date.today()-timedelta(days=2)).split(" ")[0]:
    #     print("Not refreshing")
    #     return all_tweets
    # else:
    #     print("Refreshing")
    #     all_tweets.write(str(date.today())) # Put date of tweet retrieval at top of file.
    #     all_tweets.write("\n\n")
    #     for tweet in timeline:
    #         all_tweets.write(str(tweet.full_text.encode("utf8")))
    #         all_tweets.write("\n")
    #     return all_tweets

get_tweets("zachary3352")

#print("You've liked", user.favourites_count, "tweets.")
