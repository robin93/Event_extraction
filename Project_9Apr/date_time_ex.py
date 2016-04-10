import datetime
import re
from collections import defaultdict

def normalize_text(text):
    try:
        text = text.encode('utf-8')
    except: pass
       #text = text.replace("-", " ")
       #normalize some utf8 encoding
    text = text.replace("\x9d",' ').replace("\x8c",' ')
    text = text.replace("\xa0",' ')
    text = text.replace("\x9d\x92", ' ').replace("\x9a\xaa\xf0\x9f\x94\xb5", ' ').replace("\xf0\x9f\x91\x8d\x87\xba\xf0\x9f\x87\xb8", ' ').replace("\x9f",' ').replace("\x91\x8d",' ')
    text = text.replace("\xf0\x9f\x87\xba\xf0\x9f\x87\xb8",' ').replace("\xf0",' ').replace('\xf0x9f','').replace("\x9f\x91\x8d",' ').replace("\x87\xba\x87\xb8",' ')        
    text = text.replace("\xe2\x80\x94",' ').replace("\x9d\xa4",' ').replace("\x96\x91",' ').replace("\xe1\x91\xac\xc9\x8c\xce\x90\xc8\xbb\xef\xbb\x89\xd4\xbc\xef\xbb\x89\xc5\xa0\xc5\xa0\xc2\xb8",' ')
    text = text.replace("\xe2\x80\x99s", " ").replace("\xe2\x80\x98", ' ').replace("\xe2\x80\x99", ' ').replace("\xe2\x80\x9c", " ").replace("\xe2\x80\x9d", " ")
    text = text.replace("\xe2\x82\xac", " ").replace("\xc2\xa3", " ").replace("\xc2\xa0", " ").replace("\xc2\xab", " ").replace("\xf0\x9f\x94\xb4", " ").replace("\xf0\x9f\x87\xba\xf0\x9f\x87\xb8\xf0\x9f", "")
    return text

def date_time_extract(tweet):
    pattern = re.compile("(\d{1,2}((:\d{2})*(am|pm)*(-\d{1,2}(:\d{2})*(am|pm))*))",re.I)
    datereg = re.compile("\d{1,2}\/\d{1,2}|tomorrow|tmrw|yesterday|tonight|today",re.I)
    tomorrowreg = re.compile("tomorrow|tmrw",re.I)
    today = re.compile("today|tonight",re.I)
    datereg2 = re.compile("\d{1,2}\/\d{1,2}",re.I)
    conj1reg = re.compile("-|thru|btn",re.I)
    conj2reg = re.compile("\+|&|and",re.I)
    
    ##extract time and mark positions
    string = normalize_text(tweet[1])
    string = str(string)
    result = re.findall(pattern,string)
    time = []
    for res in re.finditer(pattern,string):
        if len(res.group())>=3:
            start = res.span()[0]
            end = res.span()[1]
            time.append([res.group(),[start,end]])

    ##extract date and mark positions
    matchdate = re.findall(datereg,string)
    string1 = tweet[0]
    date1 = []
    for i in range(0,len(matchdate)):
        if re.match(tomorrowreg,matchdate[i]) != None:
            temptime = string1 + datetime.timedelta(days=1)
        elif re.match(today,matchdate[i]) != None:
            temptime = string1 + datetime.timedelta(days=0)
            
        elif re.match(datereg2,matchdate[i]) != None:
            year = string1.year
            temptime = matchdate[i]+"/"+str(year)
            temptime = datetime.datetime.strptime(temptime, "%m/%d/%Y")
        start = string.find(matchdate[i])
        end = start + len(matchdate[i])-1
        date1.append([temptime.strftime("%d-%m-%Y"),[start,end]])

    date = []
    for i in range(0,len(date1)):
        flag = 600
        for j in range(0,len(date)):
            if date1[i][0]==date[j][0]:
                flag = j
        if flag <600:
            date.pop(j)
        date.append(date1[i])
    ##join date and time
        
    date_time = {}
    date_pos = {}
    if(len(time)==0):
        for d in date:
            date_time[d[0]]="empty"
    elif(len(time)==1):
        for d in date:
            date_time[d[0]]=time[0][0]
    else:
        for t in range(0,len(time)):
            for d in date:
                if time[len(time)-1-t][1][1]>d[1][1]:
                    date_time[d[0]]=time[len(time)-1-t][0]
    for d in date:
        date_pos[d[0]]=d[1]
    
    #inverse dictionary from time to date
    time_date = defaultdict(list)
    for key, value in sorted(date_time.iteritems()):
        time_date[value].append(key)

    #conjuction check
    temp = []
    new = []
    for key in time_date:
        temp = time_date[key]
        date = 0
        while(date<len(temp)-1):
##        for date in range(0,len(temp)-1):
            lk_end = date_pos[temp[date+1]][0]
            lk_start = date_pos[temp[date]][1] + 1
            conjunction = string[lk_start:lk_end]
            if(re.search(conj1reg,conjunction) != None and (lk_end-lk_start<10)):
               new.append([temp[date]+" to "+temp[date+1],key])
               temp.pop(date+1)
               temp.pop(date)
               date = 0
            date += 1
        if len(temp)>0:
            join = ""
            for date in temp:
                join = join + " and " + date
            join = join[5:]
            new.append([join,key])
                
    return new
