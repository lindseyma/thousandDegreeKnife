import urllib2, json

def function():
    instream = open('../keys.csv','r')
    content = instream.readlines()
    instream.close()
    zKey = content[1].split(",")[1]
    q = "http://www.zillow.com/webservice/GetRegionChildren.htm?"
    q += "zws-id=" + zKey
    q += "&state=" + "wa"
    q += "&city=" + "seattle"
    q += "&childtype=" + "neighborhood"
    u = urllib2.urlopen(q)
    response = u.read()
    data = json.loads(response)
    return data

    
if __name__ == "__main__":
    print function()
        
