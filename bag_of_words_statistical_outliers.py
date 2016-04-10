import pandas as pd
import numpy as np
import csv as csv
import os
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import RegexpTokenizer

cwd = os.getcwd()

#read the data file
tweets_df = pd.read_csv('all_tweets_for_BOW.csv',sep = ",",header=0,encoding="ISO-8859-1")

"""tokens and frequency count"""
#creating tokens and counting their frequency in relevant and non-relevant tweets
#corresponging to every token a length-3 array is created
#the first element is the frequency in relevant tweet and second is frequency in non-relevant tweets and third is the difference
word_freq_dict = dict()
tknzr = TweetTokenizer()
rknzr = RegexpTokenizer(r'\w+')
iterations = 0
for index,row in tweets_df.iterrows():
	iterations += 1
	tweet = row['Tweets']
	#tokenize, convert to lower case, remove numbers and remove strings with length less than 2
	tokens = [str(i.lower()) for i in rknzr.tokenize(tweet) if (i.isalpha()== True and len(str(i.lower()))>2)]
	if row['Relevance'] == 'Relevant':
		for token in tokens:
			if token not in word_freq_dict.keys():
				word_freq_dict[token] = [1,0,0]
			else:
				word_freq_dict[token][0] += 1
	else:
		for token in tokens:
			if token not in word_freq_dict.keys():
				word_freq_dict[token] = [0,1,0]
			else:
				word_freq_dict[token][1] += 1

#Calculating the normalized value for the difference in the frequency in the relevant and non-relevant tweets
diff_value_list = list()
diff_value_list_unnormalized = list()
for words in word_freq_dict.keys():
	word_freq_dict[words][2] = float(word_freq_dict[words][0])/463 - float(word_freq_dict[words][1])/2524
	diff_value_list.append(word_freq_dict[words][2])

print diff_value_list

histo, bin_edges = np.histogram(diff_value_list,density=False)
print 'histogram values', histo
print 'bin edges value',bin_edges

"""statistical analysis on the difference values"""
##calculation the mean and standard deviation of the difference values
mean_value = np.mean(diff_value_list)
std = np.std(diff_value_list)
print mean_value
print std
# outliers = [i for i in diff_value_list if (i>mean_value+2*std or i< mean_value-2*std)]
# positive_outliers = [i for i in outliers if i>0]
# negative_outliers = [i for i in outliers if i<0]
# #calculating the lower and upper bound for selecting the difference values
# positive_min = np.min(positive_outliers)
# negative_max = np.max(negative_outliers)


# """Using the result from the statistical analysis to extract the corresponding words"""
# #Extracting the words from the list following the upper and the lower bound
# pos_word_list = list()
# neg_word_list = list()
# for word in word_freq_dict.keys():
# 	if word_freq_dict[word][2] > positive_min:
# 		pos_word_list.append(word)
# 	elif word_freq_dict[word][2] < negative_max:
# 		neg_word_list.append(word)

# print "Positive word list",pos_word_list
# print "Negative word list",neg_word_list