
#classify incoming tweet
import train_classifier as tc
import date_time_ex as dte
import read
import re
import relevant_term as rt
import location_tagger as lt
import csv
##from sklearn.metrics import confusion_matrix

# create a dictionary to store
dict_formated_output = {}

def getFormattedOutput():
        return dict_formated_output

# input the text containing tweetsummary, location , date and time.
def formatOutput(tweet_summary, location, date, time):
        date_list = date.split(" and ")

        for dt in date_list:
                if dt in dict_formated_output:
                        dict_formated_output[dt] = dict_formated_output[dt]  + " ; " + str(tweet_summary) + "|" + str(location) + "|" + str(time)
                else:
                        dict_formated_output[dt] =  str(tweet_summary) + "|" + str(location) + "|" + str(time)
        return 0

def printOutput():
        dict_data = getFormattedOutput()
        for dt in dict_data:
                rt.TRACE(dt)
                event_details = dict_data[dt].split(" ; ")
                for evnt in event_details:
                        temp = evnt.split("|")
                        rt.TRACE("Location : ",temp[1])
                        rt.TRACE("Time : ", temp[2])
                        rt.TRACE("Event Tag",temp[0])

#Run CLassifier
classpath = "classified.csv"
classifying = tc.train_classifier(classpath)

#Extract New Tweet
include_columns = [1,6,7]
filepath = "u_NYC_DOT_t_1449992629_TMLineTwt.csv"
tweets = read.file_list(filepath,include_columns)

#Tokenize - Find Feature - Classify - Extract if relevant

with open('final2.csv','wb') as f:
        writer = csv.writer(f)
        for row in tweets:
                #rt.TRACE(row[0])
                #rt.TRACE(row[1])
                #rt.TRACE(row[2])
                working_tweet = tc.tweet_Tokenizer(row[1])
                relevance = classifying[0].classify(tc.find_features(working_tweet,classifying[1]))
                #print(relevance)
	
                if(relevance == 'Relevant'):
                        date_time = dte.date_time_extract(row[0:2])
                        summary = rt.ExtractRelWordfromText(row[1])
                        #print(row)
                        locations = lt.tweet_location(row)
                        locations_string = ""
                        for loc in locations:
                                locations_string = locations_string + "," + loc
                        locations_string = locations_string[1:]
                        locations_string = re.sub(' +',' ',locations_string).lstrip()
                        initial = 0
                        for dt in date_time:
                                if(initial == 0):
                                        text = dte.normalize_text(row[1])
                                        writer.writerow([text,summary,row[2],locations_string,dt[0],dt[1]])
                                        initial = 1
                                else:
                                        writer.writerow(["","","","",dt[0],dt[1]])
                                formatOutput(summary,locations,dt[0],dt[1])
                                #rt.TRACE("Date : ",dt[0]," at ",dt[1])
                                #rt.TRACE("Address : ",locations_string)
                                #rt.TRACE("Event Tag : "+summary)
                                #print(dt[0],dt[1],summary,locations)
                                #check = input('Continue or Not:' )
printOutput()
f.close()

#confusion_matrix([1,0,0],[1,0,1])
##tweet = []
##for i in range(0,len(tweetR)):
##	if(tweetR[i] == 'Relevant'):
##		tweet.append([tweetTime[i],tweetDesc[i]])
