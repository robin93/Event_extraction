import csv
import nltk
import twokenize as tk
import datetime
import re
import numpy
from numpy import random as r

# from nltk.corpus import stopwords
# from stopwords import get_stop_words
from nltk.stem import PorterStemmer

# stop = stopwords.words('english') + get_stop_words('english')

stop = "english"

## document in terms of features - function

def find_features(document,featureset):
    words = set(document)
    features = {}
    for w in featureset:
        if w in words:
            features[w] = 1
        else:
            features[w] = 0
    return features

def tweet_Tokenizer(tweet):
    string = tweet.lower()
    punct_num = re.compile(r'[-.?!,":;()|0-9]')
    time_pat = re.compile("(\d{1,2}(.\d{1,2})|\d{1,2})(am|pm|AM|Am|PM|Pm)")
    date_pat = re.compile("\d{1,2}\/\d{1,2}")
    string = re.sub(time_pat, '', string)
    string = re.sub(date_pat, '', string)
    string = punct_num.sub("", string)
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    string = tokenizer.tokenize(string)
    string = [i for i in string if (i not in stop)]
    token = [PorterStemmer().stem(i) for i in string]
    return token
                
def train_classifier(classpath):
##ifile  = open('F:/Srinjay/Tweet Feed/Tweet Feed/classsified.csv', "rb")
    ifile  = open(classpath, "rb")
    reader = csv.reader(ifile)
    rownum = 0
    tweetTime = []
    tweetDesc = []
    tweetR = []
    tweetToken = []
    tweet = ""
    ps = PorterStemmer()
    for row in reader:
        if rownum == 0:
            header = row
        else:
            colnum = 0
            if (row[0].find("+0000")!=-1):
                tweet = row[0].lower()
                tweetR.append(row[1])
                brk = tweet.index('+0000')+10
                tweetTime.append(datetime.datetime.strptime(tweet[:brk], "%a %b %d %H:%M:%S +0000 %Y"))
                x = tweet[brk:]
                squeeze = tk.squeezeWhitespace(x)
                normal = tk.normalizeTextForTagger(squeeze.decode('utf8'))
                tweetDesc.append(normal)
                punct_num = re.compile(r'[-.?!,":;()|0-9]')
                time_pat = re.compile("(\d{1,2}(.\d{1,2})|\d{1,2})(am|pm|AM|Am|PM|Pm)")
                date_pat = re.compile("\d{1,2}\/\d{1,2}")
                week_pat = re.compile("Sun|Mon|Tue|Wed|Thurs|Fri|Sat|sunday|monday|tuesday|wednesday|thursday|friday|saturday/",re.I)
    ##            print(rownum,normal)
                if(time_pat.search(normal)):
                    normal = normal + " timepresent"
                if(date_pat.search(normal)):
                    normal = normal + " datepresent"
                if(week_pat.search(normal)):
                    normal = normal + " weekpresent"
                normal = re.sub(time_pat, '', normal)
                normal = re.sub(date_pat, '', normal)
                normal = re.sub(week_pat, '', normal)
                normal = punct_num.sub("", normal)
                tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
                b = tokenizer.tokenize(normal)
                b = [i for i in b if (i not in stop)]
                token = [ps.stem(i) for i in b]
    ##            print(rownum)
                tweetToken.append(token)
                
        rownum += 1
    ifile.close()

    ## feature engineering

    documents = []
    all_words = []
    tweet_non = []
    tweet_rel = []
    for i in range(0,len(tweetR)):
        documents.append((tweetToken[i],tweetR[i]))
        all_words.extend(tweetToken[i])
        if (tweetR[i] == 'Non-Relevant'):
            tweet_non.extend(tweetToken[i])
        else:
            tweet_rel.extend(tweetToken[i])
            
    all_words_freq = nltk.FreqDist(all_words)
    rel_words_freq = nltk.FreqDist(tweet_rel)
    non_words_freq = nltk.FreqDist(tweet_non)

    ##ranked words according to c/n ratio with add 1 smoothing

    init_features = list(all_words_freq.keys())
    score_words = []
    for i in init_features:
        score_words.append([float(rel_words_freq[i]+1)/float(non_words_freq[i]+1),i])
    score_words = sorted(score_words, reverse=True)
    scores = []
    scores = [i[0] for i in score_words]
    scores_mean = numpy.average(scores)
    features_1 = [];

    #random sample gneration 2000 - train, rest - test


    a = (r.uniform(0,len(tweetToken),2000))
    b = [int(i) for i in a]

    accu = []
    threshold = range(5,20,2)
    threshold = [float(i)/10 for i in threshold]
    threshold = 0.7
    features_1 = [];
    for i in range(0,len(score_words)):
        if score_words[i][0]>threshold:
            features_1.append(score_words[i][1])

    feature_score1=[]
    for i in range(0,len(tweetR)):
        feature_score1.append([find_features(tweetToken[i],features_1),tweetR[i]])

    trainingset = []
    for i in b:
        trainingset.append(feature_score1[i])

    testset = [x for x in feature_score1 if x not in trainingset]


    ##naive base

    naive = nltk.NaiveBayesClassifier.train(trainingset)
    accuracy = nltk.classify.accuracy(naive,testset)
    classifier = [naive,features_1,accuracy]

    return classifier

