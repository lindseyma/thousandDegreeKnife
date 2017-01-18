import urllib2, json

query = "https://data.cityofnewyork.us/resource/2fra-mtpn.json?$$app_token=TKlqxaWm34w1psikzuNcuaa2D&$select=OFNS_DESC"

def crimeCall():
	u = urllib2.urlopen(query)
	json_string = u.read()
	parsed_json = json.loads(json_string)
	return parsed_json.keys()

print crimeCall()
