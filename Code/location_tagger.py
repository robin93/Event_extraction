from geopy.geocoders import Nominatim
import re
import nltk

low = [39.914668, -79.133970]
up = [43.818746, -71.653065]

##called for each word
def location(word):
    word_m = re.sub(r"(\w)([A-Z])", r"\1 \2", word)
    geolocator = Nominatim(country_bias='USA', timeout=4)
    geocoded = geolocator.geocode(word_m, exactly_one=True)
    if geocoded is not None:
        # success
        lat = geocoded.latitude
        lon = geocoded.longitude
        if(lat<up[0] and lat>low[0] and lon<up[1] and lon>low[1]):
            locat = "New York"
        else:
            locat = "Not in New York"
        location = True
    else:
        # Here, perhaps you can run the geocoding function again,
        # after cleaning your input a little bit
        # Then you have recursion until you get a result!
        location = False
    return [location,locat,lat,lon]


##called for each tweet
def tweet_location(tweet):
    print "function called"
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
                locat.append(word)
    except Exception, e:
        print str(e)
    return locat
##    
##  a.productions().pop().rhs()[0][0]
