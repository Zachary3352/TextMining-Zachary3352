from datetime import *
import twitter
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from config import *

screen_name = input("Which username would you like to use?\n")

api = twitter.Api(consumer_key=API_key,
                  consumer_secret=API_secret_key,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret,
                  tweet_mode= 'extended')
timeline = api.GetUserTimeline(screen_name=screen_name, include_rts=0, count=199)
user = api.GetUser(screen_name=screen_name)

def get_tweets(screen_name):
    """Get a Twitter user's timeline.

    Checks if a user's tweets were retrieved more than two days ago or if the username in the text file "all_tweets.txt" is different than the chosen username.
    If either of these conditions are true, the user's tweets are re-retrieved and printed to "all_tweets.txt"
    Otherwise, the current text file is assumed to be current enough.

    Args:
        screen_name: the screen name of the user whose tweets we would like to retrieve. Automatically populated by the input prompt at the beginning of the script.

    Returns:
        A text file called "all_tweets.txt" populated with a given user's most current tweets, retrieved at most two days ago (to save API calls).
    """
    all_tweets = open("alltweets.txt", "r+")
    retrieval_date = all_tweets.readline().split("\n")[0]
    potential_screen_name = all_tweets.readline().split("\n")[0]

    if (screen_name == potential_screen_name) and (str(retrieval_date) == str(date.today()) or retrieval_date == str(date.today()-timedelta(days=1)).split(" ")[0] or retrieval_date == str(date.today()-timedelta(days=2)).split(" ")[0]):
        print("Not refreshing")
        return all_tweets
    else:
        print("Refreshing")
        all_tweets.seek(0)
        all_tweets.truncate(0)
        all_tweets.write(str(date.today())) # Put date of tweet retrieval at top of file.
        all_tweets.write("\n")
        all_tweets.write(screen_name)
        all_tweets.write("\n\n")
        for tweet in timeline:
            all_tweets.write(str(tweet.full_text.encode("utf8")))
            all_tweets.write("\n")
        return all_tweets


def words_in_file(filename):
    """Gets the words in a text file.

    Makes a list of all the words in a text file. Words are converted into lower-case.

    Args:
        filename: a text file containing words.

    Returns:
        A list of all the words in a text file.

    Examples:
        >>> words_in_file("testfile.txt")
        ['blah', 'test', 'file']
    """
    lines = []
    final_lines = []

    with open(filename, encoding="utf8") as fp:
        for line in fp:
            processed_line = line.strip()
            processed_line = processed_line.lower()
            processed_line = processed_line.split()
            lines.append(processed_line)

    for sublist in lines:
        for item in sublist:
            item = remove_punc(item)
            final_lines.append(item) # I had most of this already figured out, but a Stack Overflow answer helped a bit: https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists

    return final_lines


def remove_punc(original_string):
    """Removes punctuation from a string.

    Removes punctuation from a given string.

    Args:
        original_string: a string containing a word and potentially punctuation.

    Returns:
        A string based on original_string with punctuation removed.

    Examples:
        >>> remove_punc("...test.ing//123")
        'testing123'
    """
    temp_string = ""

    for letter in range(len(original_string)+1):
        temp_string = temp_string + original_string[letter-1:letter].strip(string.punctuation)

    return temp_string


def book_histogram(booktxtfile):
    """Makes a histogram (dictionary form) from a text file.

    Takes a text file and makes a histogram of the words in the file.

    Args:
        booktxtfile: a text file containing words, punctuation, etc.

    Returns:
        A list of all the words in a text file.

    Examples:
        >>> book_histogram("testfile.txt")
        [('blah', 1), ('test', 1), ('file', 1)]
    """
    words = words_in_file(booktxtfile)
    return histogram(words)


def histogram(wordlist):
    """Makes a histogram from a list of words.

    Takes in a list of words and makes a histogram (dictionary form) out of the list based on word frequency.

    Args:
        wordlist: a list containing words.

    Returns:
        A histogram of words based on word frequency in a list.

    Examples:
        >>> histogram(["orange", "banana", "orange", "apple"])
        [('orange', 2), ('banana', 1), ('apple', 1)]
    """
    hist = dict()

    for word in wordlist:
        hist[word] = hist.get(word, 0) + 1

    sorted_hist = sorted(hist.items(), key=lambda x: x[1], reverse=True) # I was curious about which words showed up most in the book, so I used this answer to help me sort the dictionary: https://thomas-cokelaer.info/blog/2017/12/how-to-sort-a-dictionary-by-values-in-python/

    return sorted_hist


def analyze_tweets(tweetsfile, min_occurrences):
    """Analyzes tweets in a couple ways.

    Takes in a file containing a Twitter user's tweets.
    Prints the number of tweets the user has liked since joining Twitter.
    Prints a histogram based on word frequency of the user's tweets.
    Limits the histogram to words that occur at least min_occurrences times in the file.
    Analyzes the overall sentiment of the user's tweets using NLTK's SentimentIntensityAnalyzer and prints the result.

    Args:
        tweetsfile: a text file containing tweets.
        min_occurrences: the minimum number of times a word must show up in the text file in order for the word to be used in the histogram.

    Returns:
        None, but prints results.
    """
    print("\n@", screen_name, " has liked ", user.favourites_count, " tweets.\n", sep="")

    histogram = book_histogram(tweetsfile)
    for key, value in dict(histogram).items():
        key_index = len(dict(histogram).keys())
        if value <= min_occurrences:
            del histogram[key_index-1]
    print(histogram, "\n")

    all_words = ""
    for item in words_in_file(tweetsfile):
        all_words = all_words + " " + item
    analyzer = SentimentIntensityAnalyzer()
    print(analyzer.polarity_scores(all_words), "\n")

get_tweets(screen_name)
analyze_tweets("alltweets.txt", 10)

if __name__ == '__main__': # Left this section on because when working correctly, it produces no output.
    import doctest
    doctest.testmod()
