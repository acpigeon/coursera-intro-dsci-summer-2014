import sys
import json


def get_scores():
    # create a dict with word:score key:vals
    word_scores = {}
    afinn_file = open(sys.argv[1])
    for line in afinn_file.readlines():
        word, score = line.strip().split('\t')
        word_scores[unicode(word, 'utf-8')] = int(score)
    return word_scores


def get_tweets():
    # create a list of raw tweet text
    tweets = []
    tweet_file = open(sys.argv[2])
    for line in tweet_file.readlines():
        json_line = json.loads(line)
        if 'text' not in json_line.keys():
            tweets.append('')
        else:
            tweets.append(json_line['text'])
    return tweets


def calc_sentiments():
    word_scores = get_scores()
    tweets = get_tweets()
    sentiment_scores = []

    for tweet in tweets:
        tweet_score = 0
        words = tweet.split()
        for word in words:
            if word in word_scores.keys():
                tweet_score += word_scores[word]
        sentiment_scores.append(tweet_score)

    return word_scores, tweets, sentiment_scores


if __name__ == '__main__':
    word_scores, tweets, sentiment_scores = calc_sentiments()

    for sentiment in sentiment_scores:
        print sentiment