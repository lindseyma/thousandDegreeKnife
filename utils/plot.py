import urllib, urllib2, json

query = "https://data.cityofnewyork.us/resource/2fra-mtpn.json?$select=ofns_desc,location_1"

def crimeCall():
	try:
		list = []
		u = urllib2.urlopen(query)
		data=json.load(u)
		u.close()
		for key in data:
			try:
				list.append(key['location_1']['latitude'])
				list.append(key['location_1']['longitude'])
				list.append(key['ofns_desc'])
			except:
				pass
		return list
		#return data
	except urllib2.HTTPError, e:
		return "HTTP error: {}".format(e.code)
	except urllib2.URLError, e:
		return "Network error: {}".format(e.reason.args[1])
	
	##json_string = u.read()
	##parsed_json = json.loads(json_string)
	##return parsed_json.keys()
	
print crimeCall()

