import re
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
    for i in frequencies.keys():
        #print i + ' ' + str(frequencies[i])
        print ("%s %.6f" %(i, frequencies[i]))

def main():
    words = extract_words_tweets(sys.argv[1])
    frequencies = calculate_frequencies(words)
    
    print_frequencies(frequencies)


def extract_tweets(fp):
    items = []
    with open(fp) as json_file:
        for line in json_file:
            tweet = json.loads(line)
            
            if ('text' in tweet and 'lang' in tweet and tweet.get('lang') == 'en'):
                text = tweet.get('text')
                items.append(text)
    return items

def is_word(word):
    if ":" in word: return False
    if "." in word: return False
    if "'" in word: return False
    if "," in word: return False
    if "`" in word: return False
    if "\n" in word: return False
    if "]" in word: return False
    if "?" in word: return False
    if ";" in word: return False
    if "\"" in word: return False
    if "-" in word: return False
    if "!" in word: return False

    #print ("'%s' is word %s"%(word, (not re.match('[^[a-z]+',word))))
    return (re.match('[^a-z]+', word) == None) 


def extract_words_tweets(fp):
    words = []
    tweets = extract_tweets(fp)
    for tweet in tweets:
        for word in tweet.split(' '):
            if not (word == ''):
                words.append(word.lower())
    return words
 
def calculate_frequencies(words):
    occurrences = {} 
    for word in list(words):
        if is_word(word):
            #print ("'%s' is word %s"%(word, (is_word(word))))
            if occurrences.has_key(word) == False:
                occurrences[word] = 0
            occurrences[word] = float(occurrences[word] + 1)

    sum_of_occurrences = sum(occurrences.values())
    
    frequencies = {}
    for word in occurrences.keys():
        frequencies[word] = occurrences[word] / sum_of_occurrences
        #print ("word: %s count %s\t->\t%s on %s"%(word, occurrences[word], frequencies[word], sum_of_occurrences))
    return frequencies
    


if __name__ == '__main__':
    main()
