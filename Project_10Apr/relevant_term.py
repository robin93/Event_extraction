import csv
import re


# The relevant words extracted from relevant tweets.
relevant_vocab_list = ['closures', 'closure', 'lane', 'lanes', 'location', 'locations', 'located', 'street', 'streets', 
						'boro', 'boros', 'bridge', 'bridges', 'schedule', 'scheduled', 'schedules', 'scheduling', 'check', 
						'checks', 'checked', 'closed', 'closes', 'close', 'closing', 'closely', 'repaired', 'repair', 'repairs', 
						'repairing', 'repairer', 'request', 'requests', 'requesting', 'borough', 'boroughs', 'reminder', 
						'reminding', 'remind', 'reminds', 'full', 'suspended', 'vehicle', 
						'vehicles', 'condition', 'conditions', 'plan', 'planning', 'plans', 'planned', 'route', 'routing', 
						'routes', 'routed', 'roadway', 'roadways', 'overnight', 'signal', 'signals', 'signalized', 'open', 
						'opened', 'opening', 'opens', 'openings', 'effect', 'effects', 'effective', 'using', 'used', 'use', 
						'operating', 'operate', 'operated', 'operators', 'operations', 'operates', 'operation', 'operator', 
						'operational', 'remain', 'remained', 'remains', 'detours', 'detour', 'road', 'roads', 'directions', 
						'directives', 'direction', 'directed', 'direct', 'driving', 'drive', 'drives', 'access', 'accessibility', 
						'accessible', 'continuing', 'continue', 'continues', 'continued', 'continuous', 'continuously', 'stop', 
						'stopped', 'stops', 'stopping', 'posted', 'posts', 'post', 'manhattan', 'intermittent', 'intermittently', 
						'brooklyn', 'available', 'path', 'paths', 'south', 'tube', 'north', 'meeting', 'meetings', 'meets', 'meet', 
						'resumed', 'resume', 'resumes', 'riding', 'ride', 'rides', 'rush', 'notified', 'notify', 'tunnel', 'tunnels', 
						'blocking', 'blocked', 'blocks', 'block', 'mnbound', 'speed', 'speeding', 'started', 'start', 'starting', 'starts', 
						'announcing', 'announces', 'announce', 'announcement', 'announced', 'alternate', 'alternative', 'alternatives', 
						'barriers', 'barrier', 'completed', 'complete', 'completion', 'completely', 'cross', 'crossing', 'crossings', 
						'modified', 'westbound', 'eastbound', 'alert', 'alerts', 'alerting', 'northbound', 'travel', 'traveling', 'travelers', 
						'traveler', 'rescheduled', 'reschedule', 'broadway', 'manhattanbound', 'vehicular', 'clear', 'cleared', 'clears', 
						'clearing', 'extended', 'extending', 'extend', 'level', 'restore', 'restores', 'restored', 'restoring', 'restoration', 
						'transit', 'transitioned', 'transition', 'connects', 'connect', 'connected', 'connection', 'connecting', 'connections', 
						'east', 'canceled', 'cancelled', 'cancellations', 'intersections', 'intersection', 'southbound', 'subways', 'subway', 
						'changed', 'change', 'changes', 'partial', 'partially', 'riders', 'overpass', 'overpasses', 'expressway', 'queensbound', 
						'temporary', 'bronx', 'postponed', 'carfree', 'congestion', 'congested', 'mnbd', 'bound', 'permanently', 'permanent', 
						'suspension', 'suspensions', 'temp', 'temps', 'brooklynbound', 'navigate', 'navigation', 'obstruction', 'roadwork', 
						'switch', 'failure', 'northtube', 'qnsbound', 'redirecting', 'redirection', 'bainbridge', 'bklyn', 'downtown', 'manattan', 
						'mnhtn', 'pennsylvania', 'southwest', 'struck']

manual_entry = ['traffic','shift','both']
###################################################################################
# debug vraiable. Set this flag to 1 to enable debugging. Else set to 0. 
__DEBUG__ = 1

# For testing purpose
def TRACE(*var):
    if(__DEBUG__ == 1):
        print(var)
        print("\n")
###################################################################################


# getter for vocab list
def getRelevantVocablist():
	return relevant_vocab_list

'''def create_vocab():
	with open('Selected_relevant_token_stem_freq.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		try:
			for row in reader:
				vlist = row[1].split(" ")
				for word in vlist:
					relevant_vocab_list.append(word)
		except csv.Error as e:
            		sys.exit('file %s, line %d: %s' %(fname, writer.line_num, e))
            		return e
	csvfile.close()
	return relevant_vocab_list

def find_rel_tweet(fname):

	rel_token_tweet = []
	vocablist = create_vocab()
	with open(fname, 'rb') as csvfile:
		has_header = csv.Sniffer().has_header(csvfile.read(1024))
		csvfile.seek(0)
		reader = csv.reader(csvfile)
		if(has_header):
			next(reader)		# skip the header row
		
		try:	
			with open('tweet_txt_file.csv','wb') as writefile:
				writer = csv.writer(writefile) 
				for row in reader:
					tweet_txt = row[0]
					tweet_txt = tweet_txt.lower()
					#print(tweet_txt)
					#check = input('Continue or Not:' )
					tweet_txt = tweet_txt.split(" ")
					twt_rel_words = []
					for tk in tweet_txt:
						if tk in vocablist:
							twt_rel_words.append(tk)
					writer.writerow([tweet_txt,' '.join(twt_rel_words)])
					#print(' '.join(tweet_txt),' '.join(twt_rel_words))			
			writefile.close()
		except csv.Error as e:
            		sys.exit('file %s, line %d: %s' %(fname, writer.line_num, e))
            		return e
	csvfile.close()
	return 0
'''

# Event Retrieval Function
def find_events(tweet_txt):
    
    pos_tag = CMUTweetTagger.runtagger_parse(tweet_txt)
    TRACE(pos_tag)
    return 0
# Find the exact word
def find_word(text,search):
    result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
    if(len(result)> 0):
        return 1
    else:
        return 0
                        
dict_relevant_tokens = {}
dict_relevant_stm_tokens = {}
dict_relevant_stm_token_pair = {}

# Extract Only Relevant Tweets and save in a file
def relevant_tweets(text):
    for tk in text:
        stem_word = ps.stem(tk)

        if stem_word in dict_relevant_stm_token_pair:
            if(find_word(dict_relevant_stm_token_pair[stem_word],tk) == 0):
                dict_relevant_stm_token_pair[stem_word] = dict_relevant_stm_token_pair[stem_word] + " " + tk
        else:
            dict_relevant_stm_token_pair[stem_word] = tk
            
        if stem_word in dict_relevant_stm_tokens:
            dict_relevant_stm_tokens[stem_word] += 1
        else:
            dict_relevant_stm_tokens[stem_word] = 1
            
        if tk in dict_relevant_tokens:
            dict_relevant_tokens[tk] +=1
        else:
            dict_relevant_tokens[tk] = 1
        #TRACE(t)
        
    return 0

# File writer module using data as dictionary
def write_file(fname, dict_data):
    with open(fname, 'wb') as f:
        writer = csv.writer(f)
        try:
            for key in dict_data:
                writer.writerow([key, dict_data[key]])
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' %(fname, writer.line_num, e))
            return e
    
    f.close()
    return 0

# tweets_list contains the [tweetTime(Date Format), tweetText (String), tweetHash (String)]
def ExtractRelWordfromText(text):
	
	vocablist = getRelevantVocablist()

	tweet_txt = text
	tweet_txt = tweet_txt.lower()
	tweet_txt = tweet_txt.split(" ")
	twt_rel_words = []
	
	for tk in tweet_txt:
		if tk in vocablist:
			twt_rel_words.append(tk)
	
	twt_rel_words = ' '.join(twt_rel_words)
	return twt_rel_words


#print(create_vocab())
'''with open('event_vocab_2.csv','wb') as csvfile:
	wtr = csv.writer(csvfile)
	for tk in relevant_vocab_list:
		wtr.writerow([tk])
	csvfile.close()'''
#find_rel_tweet('relevant_tweets.csv')
	
#print(' '.join(relevant_vocab_list))
