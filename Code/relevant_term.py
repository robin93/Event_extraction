import csv
import re


# The relevant words extracted from relevant tweets.
relevant_vocab_list = ['access', 'accessibility', 'accessible', 'alert', 'alerts', 'alerting', 'alternate', 'alternative', 'alternatives', 
        'announcing', 'announces', 'announce', 'announcement', 'announced', 'available', 'avoid', 'bainbridge', 'barriers', 
        'barrier', 'began', 'begin', 'begins', 'beginning', 'bike', 'biking', 'bikes', 'bklyn', 'blocking', 'blocked', 
        'blocks', 'block', 'boardwalk', 'boro', 'boros', 'borough', 'boroughs', 'bound', 'bridge', 'bridges', 'broadway', 
        'broken', 'bronx', 'brooklyn', 'brooklynbound', 'brooklynbridgeoutreach', 'business', 'busy', 'businesses', 
        'canceled', 'cancelled', 'cancellations', 'carfree', 'changed', 'change', 'changes', 'check', 'checks', 'checked', 
        'clear', 'cleared', 'clears', 'clearing', 'closed', 'closes', 'close', 'closing', 'closely', 'closures', 'closure', 
        'commuters', 'commute', 'commuter', 'completed', 'complete', 'completion', 'completely', 'condition', 'conditions', 
        'congestion', 'congested', 'connects', 'connect', 'connected', 'connection', 'connecting', 'connections', 'continuing', 
        'continue', 'continues', 'continued', 'continuous', 'continuously', 'coordinator', 'coordinators', 'cross', 'crossing', 
        'crossings', 'days', 'day', 'departure', 'details', 'detail', 'detours', 'detour', 'directions', 'directives', 'direction',
        'directed', 'direct', 'dismount', 'disruptions', 'downtown', 'driving', 'drive', 'drives', 'drivers', 'driver', 'east', 
        'eastbound', 'effect', 'effects', 'effective', 'event', 'events', 'expressway', 'extended', 'extending', 'extend', 
        'extensions', 'extension', 'extensive', 'failure', 'follow', 'following', 'forecasted', 'forecast', 'full', 'half', 'hall', 
        'head', 'headed', 'heads', 'intermittent', 'intermittently', 'interruptions', 'intersections', 'intersection', 'item', 
        'kbridge', 'killed', 'lane', 'lanes', 'level', 'lifted', 'location', 'locations', 'located', 'madison', 'manattan', 
        'maneuverability', 'manhattan', 'manhattanbound', 'meeting', 'meetings', 'meets', 'meet', 'mnbd', 'mnbound', 'mnhtn', 
        'modified', 'multifunction', 'navigate', 'navigation', 'north', 'northbound', 'northtube', 'notified', 'notify', 'nyc', 
        'obstruction', 'open', 'opened', 'opening', 'opens', 'openings', 'operating', 'operate', 'operated', 'operators', 'operations', 
        'operates', 'operation', 'operator', 'operational', 'overnight', 'overpass', 'overpasses', 'partial', 'partially', 'passenger', 
        'passengers', 'path', 'paths', 'pennsylvania', 'permanently', 'permanent', 'plan', 'planning', 'plans', 'planned', 'posted', 
        'posts', 'post', 'postponed', 'qnsbound', 'queensbound', 'queue', 'redirecting', 'redirection', 'remain', 'remained', 'remains', 
        'reminder', 'reminding', 'remind', 'reminds', 'reopened', 'reopen', 'reopening', 'repaired', 'repair', 'repairs', 'repairing', 
        'repairer', 'request', 'requests', 'requesting', 'requires', 'require', 'rescheduled', 'reschedule', 'restore', 'restores', 
        'restored', 'restoring', 'restoration', 'resumed', 'resume', 'resumes', 'riding', 'ride', 'rides', 'riders', 'road', 'roads', 
        'roadway', 'roadways', 'roadwork', 'roundabout', 'roundabouts', 'route', 'routing', 'routes', 'routed', 'routine', 'rush', 
        'schedule', 'scheduled', 'schedules', 'scheduling', 'signal', 'signals', 'signalized', 'slow', 'slows', 'south', 'southbound', 
        'southwest', 'speed', 'speeding', 'started', 'start', 'starting', 'starts', 'stop', 'stopped', 'stops', 'stopping', 'stoplight', 
        'street', 'streets', 'struck', 'subways', 'subway', 'suggestion', 'suggestions', 'suggested', 'suggest', 'suspended', 'suspension', 
        'suspensions', 'switch', 'temp', 'temps', 'temporary', 'thru', 'time', 'times', 'timing', 'today', 'tomorrow', 'tonight', 'transit', 
        'transitioned', 'transition', 'travel', 'traveling', 'travelers', 'traveler', 'trouble', 'tube', 'tunnel', 'tunnels', 'using', 'used', 
        'use', 'vehicle', 'vehicles', 'vehicular', 'week', 'weeks', 'weekend', 'weekends', 'westbound']

# getter for vocab list
def getRelevantVocablist():
        return relevant_vocab_list

def create_vocab():
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
# tweets_list contains the [tweetTime(Date Format), tweetText (String), tweetHash (String)]
def ExtractRelWordfromText(tweet_list):
	
	vocablist = getRelevantVocablist()

	tweet_txt = tweet_list[1]
	tweet_txt = tweet_txt.lower()
	tweet_txt = tweet_txt.split(" ")
	twt_rel_words = []
	
	for tk in tweet_txt:
		if tk in vocablist:
			twt_rel_words.append(tk)
	
	twt_rel_words = ' '.join(twt_rel_words)
	return twt_rel_words


#print(create_vocab())
'''
with open('event_vocab_2.csv','wb') as csvfile:
	wtr = csv.writer(csvfile)
	for tk in relevant_vocab_list:
		wtr.writerow([tk])
	csvfile.close()
'''
#find_rel_tweet('relevant_tweets.csv')
	
#print(' '.join(relevant_vocab_list))'''