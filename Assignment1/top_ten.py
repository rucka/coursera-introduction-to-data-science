from operator import itemgetter 
import functools
import itertools
import json
import sys

def lines(fp):
    print str(len(fp.readlines()))

def prints(items):
    for i in items:
        print i

def print_frequencies(frequencies):
    for i in frequencies:
        print ("%s %.0f" %(i[0], i[1]))

def main():
    words = extract_hashtags(sys.argv[1])
    frequencies = sorted(calculate_frequencies(words).items(), key = itemgetter(1), reverse=True)
    
    print_frequencies(frequencies[0:10])


def extract_hashtags(fp):
    items = []
    with open(fp) as json_file:
        for line in json_file:
            tweet = json.loads(line)

            if not('entities' in tweet) or not ('lang' in tweet) or not (tweet.get('lang') == 'en'): continue
            entities = tweet.get('entities')

            if ('hashtags' in entities):
                for ht in entities.get('hashtags'):
                    text = ht.get('text')
                    if "\u" in text : continue
                    items.append(text)
    return items


def calculate_frequencies(words):
    occurrences = {} 
    for word in list(words):
        if occurrences.has_key(word) == False:
            occurrences[word] = 0
        occurrences[word] = (occurrences[word] + 1)

    return occurrences 
    


if __name__ == '__main__':
    main()
