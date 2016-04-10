import datetime
import re
from collections import defaultdict

def date_time_extract(tweet):
    pattern = re.compile("(\d{1,2}((:\d{2})*(am|pm)*(-\d{1,2}(:\d{2})*(am|pm))*))",re.I)
    datereg = re.compile("\d{1,2}\/\d{1,2}|tomorrow|tmrw|yesterday|tonight|today",re.I)
    tomorrowreg = re.compile("tomorrow|tmrw",re.I)
    today = re.compile("today|tonight",re.I)
    datereg2 = re.compile("\d{1,2}\/\d{1,2}",re.I)
    conj1reg = re.compile("-|thru|btn",re.I)
    conj2reg = re.compile("\+|&|and",re.I)
    
    ##extract time and mark positions
    string = str(tweet[1])
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
        for date in range(0,len(temp)-1):
            lk_end = date_pos[temp[date+1]][0]
            lk_start = date_pos[temp[date]][1] + 1
            conjunction = string[lk_start:lk_end]
            if(re.search(conj1reg,conjunction) != None and (lk_end-lk_start<10)):
               new.append([temp[date]+" to "+temp[date+1],key])
               temp.pop(date+1)
               temp.pop(date)
        if len(temp)>0:
            join = ""
            for date in temp:
                join = join + " and " + date
            join = join[5:]
            new.append([join,key])
                
    return new
