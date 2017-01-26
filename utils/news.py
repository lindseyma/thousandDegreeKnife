import urllib2, json

def newsCall(APIKey):
  query = "https://api.nytimes.com/svc/topstories/v2/nyregion.json?api-key=" + APIKey
  u = urllib2.urlopen(query)
  data = u.read()
  u.close()
  return data
