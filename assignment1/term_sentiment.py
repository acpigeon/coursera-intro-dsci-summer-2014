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

    return sentiment_scores


def get_unscored_words():
    word_scores = get_scores()
    tweet_text = get_tweets()

    unscored_words = {}

    # identify unscored words
    for tweet in tweet_text:
        for word in tweet.split():
            if word not in word_scores.keys():
                if word not in unscored_words.keys():  # add word and set initial values
                    unscored_words[word] = {'positive_counts': 0, 'negative_counts': 0}
    return unscored_words


if __name__ == '__main__':

    #print "starting..."

    unscored_words = get_unscored_words()
    #print "acquired unscored words..."
    #print type(unscored_words)
    #print len(unscored_words)
    #print unscored_words
    #print ""

    tweets = get_tweets()
    #print "acquired tweets..."
    #print type(tweets)
    #print len(tweets)
    #print tweets[0:10]
    #print ""

    sentiment_scores = calc_sentiments()
    #print "acquired sentiment scores..."
    #print type(sentiment_scores)
    #print len(sentiment_scores)
    #print sentiment_scores[0:1000]
    #print ""

    """
    *** Scoring Overview ***
    For each tweet, see whether the overall sentiment is positive or negative
    For each unscored word in that tweet, +1 either the positive or negative count based on sentiment +/-
    For each unscored word, estimate a sentiment score as follows:
    - if pos == neg, score = 0
    - if pos > neg, score = 0.5
    - if pos < neg, score = -0.5
    Use the 0.5 because in theory these words weren't important enough to be manually scored,
    so they should count for less than the words in AFINN.
    """

    #print "starting to count unscored words..."
    for tweet, score in zip(tweets, sentiment_scores):

        # get counts of occurrences of unscored words in positive and negative tweets
        for word in tweet.split():
            if word in unscored_words.keys():
                if score > 0:
                    unscored_words[word]['positive_counts'] += 1
                if score < 0:
                    unscored_words[word]['negative_counts'] += 1

    #print "starting to score unscored words..."
    # give word a score based on prevailing sentiment
    for word in unscored_words.keys():
        if unscored_words[word]['positive_counts'] > unscored_words[word]['negative_counts']:
            unscored_words[word]['score'] = 0.5
        elif unscored_words[word]['positive_counts'] < unscored_words[word]['negative_counts']:
            unscored_words[word]['score'] = -0.5
        else:
            unscored_words[word]['score'] = 0.0

        print word + " " + str(unscored_words[word]['score'])