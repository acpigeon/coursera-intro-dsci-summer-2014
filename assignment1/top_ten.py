__author__ = 'acpigeon'

import json
import sys

def get_hashtags():
    # create a list of raw tweet text
    hashtags = {}
    tweet_file = open(sys.argv[1])
    for line in tweet_file.readlines():
        json_line = json.loads(line)
        if 'delete' not in json_line.keys():
            hash_tag_list = json_line['entities']['hashtags']
            if hash_tag_list != []:
                for hash in hash_tag_list:
                    if hash['text'] not in hashtags.keys():
                        hashtags[hash['text']] = float(0)
                    if hash['text'] in hashtags.keys():
                        hashtags[hash['text']] += float(1)
    return hashtags


if __name__ == '__main__':
    hashes = get_hashtags()
    sorted_hashes = sorted(hashes.items(), key=lambda x: x[1])[-10:]

    for hash in reversed(sorted_hashes):
        print hash[0] + " " + str(hash[1])

