
#classify incoming tweet
import train_classifier as tc
import date_time_ex as dte
import read
import relevant_term as rt
import location_tagger as lt

#Run CLassifier
classpath = "CSV/classsified.csv"
classifying = tc.train_classifier(classpath)

#Extract New Tweet
include_columns = [1,6,7]
filepath = "CSV/u_NYC_DOT_t_1449992629_TMLineTwt.csv"
tweets = read.file_list(filepath,include_columns)

#Tokenize - Find Feature - Classify - Extract if relevant
working_tweet = tc.tweet_Tokenizer(tweets[1][1])
relevance = classifying[0].classify(tc.find_features(working_tweet,classifying[1]))

if(relevance == 'Relevant'):
    date_time = dte.date_time_extract(tweets[1][0:2])
    # summary = rt.ExtractRelWordfromText(tweets[1])
    locations = lt.tweet_location(tweets[1])




##tweet = []
##for i in range(0,len(tweetR)):
##	if(tweetR[i] == 'Relevant'):
##		tweet.append([tweetTime[i],tweetDesc[i]])
