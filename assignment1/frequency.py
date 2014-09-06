__author__ = 'acpigeon'

import json
import sys

def get_tweets():
    # create a list of raw tweet text
    tweets = []
    tweet_file = open(sys.argv[1])
    for line in tweet_file.readlines():
        json_line = json.loads(line)
        if 'text' not in json_line.keys():
            tweets.append('')
        else:
            tweets.append(json_line['text'])
    return tweets

if __name__ == '__main__':

    # The frequency of a term can be calculated as [# of occurrences of the term in all tweets]/[# of occurrences of all terms in all tweets]

    tweets = get_tweets()

    histogram = {}

    for tweet in tweets:
        for word in tweet.split():
            if word not in histogram.keys():
                histogram[word] = {'count': 1.0}
            if word in histogram.keys():
                histogram[word]['count'] += 1.0

    count_all_occurrences = 0
    for word in histogram.keys():
        count_all_occurrences += histogram[word]['count']

    for word in histogram.keys():
        histogram[word]['frequency'] = float(histogram[word]['count'] / count_all_occurrences)
        print word, " ", histogram[word]['frequency']