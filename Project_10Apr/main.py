
#classify incoming tweet
import train_classifier as tc
import date_time_ex as dte
import read
import re
import relevant_term as rt
import location_tagger as lt
import csv
import geopy
from geopy.geocoders import Nominatim
import nltk
import subseq

# longitude latitude boundary for new york
low = [39.914668, -79.133970]
up = [43.818746, -71.653065]
##from sklearn.metrics import confusion_matrix
def location(word):
        word_m = re.sub(r"(\w)([A-Z])", r"\1 \2", word) #to break words like NewYork = New York
        geolocator = Nominatim(country_bias='USA', timeout=4)
        geocoded = geolocator.geocode(word_m, exactly_one=True)
        locat = ""
        lat = 0
        lon = 0
        actual = word_m
        if geocoded is not None:
        # success
                lat = geocoded.latitude
                lon = geocoded.longitude
                print("Coordinates Fetched: ",lat,lon)
                print("Checking whether the coordinates lie in NY\n\n")
                if(lat<up[0] and lat>low[0] and lon<up[1] and lon>low[1]):
                    locat = "New York"
                    tempadd = geolocator.reverse(str(lat)+","+str(lon)).address
                    print("Actual Location: ",tempadd)
                    tempadd = tempadd.split(",")
                    for i in tempadd:
                        m = len(word_m)
                        n = len(i)
                        if (subseq.isSubSequence(word_m, i, m, n) and len(tempadd)>5):
                            actual = i
                else:
                    locat = "Not in New York"
                location = True
        else:
        # Here, perhaps you can run the geocoding function again,
        # after cleaning your input a little bit
        # Then you have recursion until you get a result!
                location = False
        return [location,locat,actual]

def tweet_location(tweet):
        text = tweet[1]
        hasht = tweet[2]
        week_pat = re.compile("Sun|Mon|Tue|Wed|Thurs|Fri|Sat|sunday\w*|monday\w*|tuesday\w*|wednesday\w*|thursday\w*|friday\w*|saturday\w*",re.I)
        for res in re.finditer(week_pat,text):
        text = text.replace(res.group(),"")
        words = []
        locat = []
        try:
        tk = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tk)
        for tag in tagged:
            if tag[1] == 'NNP':
                words.append(tag[0])
        hasht = hasht.split(",")
        words = words + hasht
        for word in words:
            loc = location(word)
            if loc[0] and loc[1]=='New York':
                locat.append(loc[2])
                print("Final Location: ",loc[2],"\n\n")
        except Exception, e:
        print str(e)
        return locat


#Run CLassifier
classpath = "CSV/classified.csv"
classifying = tc.train_classifier(classpath)

#Extract New Tweet
include_columns = [1,6,7]
filepath = "CSV/u_NYC_DOT_t_1449992629_TMLineTwt.csv"
tweets = read.file_list(filepath,include_columns)
newtweets = tweets[:30]
#Tokenize - Find Feature - Classify - Extract if relevant

with open('final2.csv','wb') as f:
        writer = csv.writer(f)
        for row in newtweets:
                #rt.TRACE(row[0])
                #rt.TRACE(row[1])
                #rt.TRACE(row[2])
                working_tweet = tc.tweet_Tokenizer(row[1])
                relevance = classifying[0].classify(tc.find_features(working_tweet,classifying[1]))
                #print(relevance)
                print("Tweet is: ",relevance)
                if(relevance == 'Relevant'):
                        date_time = dte.date_time_extract(row[0:2])
                        print("Date Extracted: ",date_time)
                        summary = rt.ExtractRelWordfromText(row[1])
                        # print(row)
                        # locations = lt.tweet_location(row)
                        locations = tweet_location(row)
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
                                #print(dt[0],dt[1],summary,locations)
                                #check = input('Continue or Not:' )
f.close()

#confusion_matrix([1,0,0],[1,0,1])
##tweet = []
##for i in range(0,len(tweetR)):
##	if(tweetR[i] == 'Relevant'):
##		tweet.append([tweetTime[i],tweetDesc[i]])
