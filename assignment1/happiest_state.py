__author__ = 'acpigeon'

import json
import sys

def getStates():
    state_codes = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    state_names = {
        'Alaska': 'AK',
        'Alabama': 'AL',
        'Arkansas': 'AR',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'District of Columbia': 'DC',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Iowa': 'IA',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Massachusetts': 'MA',
        'Maryland': 'MD',
        'Maine': 'ME',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Missouri': 'MO',
        'Northern Mariana Islands': 'MP',
        'Mississippi': 'MS',
        'Montana': 'MT',
        'National': 'NA',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Nebraska': 'NE',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'Nevada': 'NV',
        'New York': 'NY',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Virginia': 'VA',
        'Virgin Islands': 'VI',
        'Vermont': 'VT',
        'Washington': 'WA',
        'Wisconsin': 'WI',
        'West Virginia': 'WV',
        'Wyoming': 'WY'
    }
    return state_codes, state_names


def get_word_sentiments():
    word_sentiments = {}
    afinn_file = open(sys.argv[1])
    for line in afinn_file.readlines():
        word, score = line.strip().split('\t')
        word_sentiments[unicode(word, 'utf-8')] = int(score)
    return word_sentiments


def load_tweets():
    tweets = []
    tweet_file = open(sys.argv[2])
    for line in tweet_file.readlines():
        json_line = json.loads(line)
        if 'delete' not in json_line.keys() and 'status_withheld' not in json_line.keys():
            tweets.append(json_line)
    return tweets


def get_tweet_sentiment(tweet, word_sentiments):
    tweet_sentiment = 0
    for word in tweet.split():
        if word in word_sentiments.keys():
            tweet_sentiment += word_sentiments[word]
    return tweet_sentiment


def filter_us_locations(tweets):

    # country_code seems most reliable
    us_tweets = []
    for tweet in tweets:
        if tweet['place'] is not None and tweet['place']['country_code'] == 'US':

            # Testing
            """
            full_name = tweet['place']['full_name']
            country = tweet['place']['country']
            place_type = tweet['place']['place_type']
            country_code = tweet['place']['country_code']
            name = tweet['place']['name']
            print ""
            print "full_name: " + full_name
            print "country: " + country
            print "place_type: " + place_type
            print "country_code: " + country_code
            print "name: " + name
            """
            us_tweets.append(tweet)
    return us_tweets


if __name__ == '__main__':

    state_codes, state_names = getStates()
    sentiment_data = get_word_sentiments()
    all_tweets = load_tweets()

    # Filter out tweets without loc info
    us_tweets = filter_us_locations(all_tweets)

    for tweet in us_tweets:
        sentiment = get_tweet_sentiment(tweet['text'], sentiment_data)
        tweet['sentiment'] = sentiment

        # start extracting a usable location. use the first one we find.
        sentiment_location = ''

        if len(tweet['place']['full_name'].split(", ")[1]) == 2 and tweet['place']['full_name'].split(", ")[1] in state_codes.keys():
            sentiment_location = tweet['place']['full_name'].split(", ")[1]
        elif tweet['place']['full_name'].split(", ")[1] in state_names.keys():
            sentiment_location = state_names[tweet['place']['full_name'].split(", ")[1]]
        elif tweet['place']['full_name'].split(", ")[0] in state_names.keys():
            sentiment_location = state_names[tweet['place']['full_name'].split(", ")[0]]

        tweet['sentiment_location'] = sentiment_location

    output = {}

    for tweet in us_tweets:
        if tweet['sentiment_location'] != '':
            if tweet['sentiment_location'] not in output.keys():
                output[tweet['sentiment_location']] = {'tweet_count': 1, 'tweet_sentiment_sum': tweet['sentiment']}
            if tweet['sentiment_location'] in output.keys():
                output[tweet['sentiment_location']]['tweet_count'] += 1
                output[tweet['sentiment_location']]['tweet_sentiment_sum'] += tweet['sentiment']

    highest_average = [0, 0]
    for state in output.keys():
        avg = float(output[state]['tweet_sentiment_sum']) / float(output[state]['tweet_count'])
        #print state + " " + str(avg)
        if avg > highest_average[1]:
            highest_average[0] = state
            highest_average[1] = float(output[state]['tweet_sentiment_sum']) / float(output[state]['tweet_count'])

    print highest_average[0]
    # Testing
    """
    for tweet in us_tweets:
        if tweet['sentiment_location'] == '':
            print tweet['sentiment']
            print tweet['place']['full_name']
            print tweet['place']['country']
            print tweet['place']['place_type']
            print tweet['place']['country_code']
            print tweet['place']['name']
            print ""
    """


    #for loc in location_data:
    #    print json.dumps(loc, sort_keys=True, indent=4, separators=(',', ': '))