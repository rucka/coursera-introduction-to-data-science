import itertools
import json
import sys

def lines(fp):
    print str(len(fp.readlines()))

def prints(items):
    for i in items:
        print i

def print_sentiments(sentiments):
    for i in sentiments.keys():
        print i + ' ' + str(sentiments[i])

def main():
    scores = extract_scores(sys.argv[1])
    tweets = extract_tweets(sys.argv[2])
    
    sentiments = calculate_missing_scores(tweets, scores)
    
    print_sentiments(sentiments)


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
def echo(x):
    print x

def calculate_missing_scores(tweets, scores):
    sentiments = list(calculate_sentiments(tweets, scores))    
    
    missings = {}
    i = 0
    for tweet in tweets:
        tweetscore = sentiments[i]
        for w in tweet.split(' '):
            word = w.lower()
            
            if (scores.has_key(word) == True):
                continue

            if (missings.has_key(word) == False):
                missings[word] = {'pos':0, 'neg':0}               

            if tweetscore > 0 :
                missings[word]['pos'] = (missings[word]['pos'] + 1)

            if tweetscore < 0 :
                missings[word]['neg'] = (missings[word]['neg'] + 1)

        i = i + 1     
    
    terms = {}
    for word in missings.keys():
        metrics = missings[word]
        pos = metrics['pos']
        neg = metrics['neg']

        if (pos + neg) == 0:
           sentiment = 0
        else:
           sentiment = float(pos - neg) / float(pos + neg) * 5
        terms[word] = sentiment
        '''
        if pos > 0 and neg > 0:
            print ("%s\t\t\t\tpos:%s\tneg:%s\tsentiment:%s"%(word, str(pos), str(neg), str(sentiment))) 
        '''
    return terms


if __name__ == '__main__':
    main()
