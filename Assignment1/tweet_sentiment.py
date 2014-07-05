import itertools
import json
import sys

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def prints(items):
    for i in items:
        print i

def main():
    '''
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)
    '''

    scores = extract_scores(sys.argv[1])
    tweets = extract_tweets(sys.argv[2])

    sentiments = list(calculate_sentiments(tweets, scores))
    
    prints(sentiments) 
    

def extract_scores(fp):
    sent_file = open(fp)
    scores = {}
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores

def extract_tweets(fp):
   items = []
   with open(fp) as json_file:
       for line in json_file:
           tweet = json.loads(line)
           
           if ('text' in tweet and 'lang' in tweet and tweet.get('lang') == 'en'):
               text = tweet.get('text')
               items.append(text)
   return items 

def calculate_sentiments(tweets, scores):
    for tweet in tweets:
        sentiment = 0
        for word in tweet.split(' '):
            if (scores.has_key(word.lower()) == True):
                sentiment = sentiment + int(scores.get(word.lower()))
            yield sentiment


if __name__ == '__main__':
    main()
