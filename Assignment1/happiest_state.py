from operator import itemgetter
import itertools
import json
import sys

states = {
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

def print_averages(averages):
        for i in averages:
            print i[0] + ' ' + str(i[1])


def prints(items):
    i = 0
    for it in items:
        i = i + 1
        print it

def main():
    scores = extract_scores(sys.argv[1])
    tweets = extract_tweets(sys.argv[2])

    #tweets = tweets[0:10]

    sentiments = list(calculate_sentiments(tweets, scores))
    states = list(extract_states(sys.argv[2])) 
    
    states_average = calculate_average(sentiments, states)
    states_average = sorted(states_average.items(), key = itemgetter(1), reverse=True)
        
    #print_averages(states_average[0:1])
    print states_average[0:1][0][0]
    #prints(states)
    #prints(tweets) 
    #prints(sentiments) 
    

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
               text = tweet.get('text').replace('\n', '<br />')
               items.append(text)
   return items 

def extract_states(fp):
   items = []
   with open(fp) as json_file:
       for line in json_file:
           tweet = json.loads(line)
           
           if not ('text' in tweet and 'lang' in tweet and tweet.get('lang') == 'en'):continue
           
           state = extract_state_from_place(tweet)
           if not state == None:
               items.append(state)
               continue
           state = extract_state_from_user(tweet)
           if not state == None:
               items.append(state)
               continue
           items.append('--')
            
   return items 

def calculate_average(sentiments, states):
    i = 0
    calculations = {}
    for item in states:
        if item == '--': continue;

        if calculations.has_key(item) == False:
            calculations[item] = {'count': 0, 'sum': 0, 'average': 0}
        count = calculations[item]['count'] 
        tot = calculations[item]['sum']
        avg = calculations[item]['average']
 
        calculations[item]['average'] = float(tot + sentiments[i]) / float(count + 1)
        calculations[item]['sum'] = tot + sentiments[i]
        calculations[item]['count'] = count + 1

        i = i + 1

    averages = {}
    for item in calculations:
        averages[item] = calculations[item]['average']
    return averages
    

def extract_state_from_place(tweet):
    if not 'place' in tweet:
        return None
            
    place = tweet.get('place')

    if place == None or not 'full_name' in place: return None  
    if not 'country_code' in place: return None  
    if not 'place_type' in place: return None  
    
    if not place.get('country_code') == "US": 
        return None
    if not place.get('place_type') == "city":
        return None
    fullname = place.get('full_name')
    state = fullname[-2:]
    if states.has_key(state) == False: return None

    #print "%s - %s - %s - %s"% (state, fullname, states.has_key(state), states[state]) 
    return state

def extract_state_from_user(tweet):
    if not 'user' in tweet:
        return None
            
    user = tweet.get('user')

    if user == None or not 'location' in user: return None  
    fullname = user.get('location')
    state = fullname[-2:]
    if states.has_key(state) == False: return None

    #print "%s - %s - %s - %s"% (state, fullname, states.has_key(state), states[state]) 
    return state

def calculate_sentiments(tweets, scores):
    for tweet in tweets:
        sentiment = 0
        for word in tweet.split(' '):
            if (scores.has_key(word.lower()) == True):
                sentiment = sentiment + int(scores.get(word.lower()))
        yield sentiment


if __name__ == '__main__':
    main()
