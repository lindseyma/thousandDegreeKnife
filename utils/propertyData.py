import urllib2, json, re
from pprint import pprint
from bs4 import BeautifulSoup

with open('../data/policeprecincts.json') as data_file:    
     data = json.load(data_file)


# converts a row string to a list of coordinates
def strTolist(string):
	rowList = []
	for x in re.split(r'[()]', string):
		if len(x) > 3:
			for y in x.split(", "):
				rowList.append(y.split(" "))
	return rowList

# creates a list of all the coordinates in the file
def genCoordinateList():
	rowNum = 0
	allRows = []
	while rowNum < len(data["data"]):
		data["data"][rowNum][10] = data["data"][rowNum][10][13:]
		allRows.append(strTolist(data["data"][rowNum][10]))
		rowNum += 1
	allCoords = []
	for row in allRows:
		for coordinate in row:
			lat = (float)(coordinate[1])
			lon = (float)(coordinate[0])
			allCoords.append([lat, lon])
	return allCoords

# checks if a given address/zipcode corresponds to a 
# property in the Zillow database
def isProperty(address, zipcode):
    address = address.replace(" ", "+")
    instream = open('../keys.csv','r')
    content = instream.readlines()
    instream.close()
    zKey = content[1].split(",")[1].strip("\n")
    q = "http://www.zillow.com/webservice/GetSearchResults.htm?"
    q += "zws-id=" + zKey
    q += "&address=" + address
    q += "&citystatezip=" + zipcode
    u = urllib2.urlopen(q)
    response = u.read()
    soup = BeautifulSoup(response, "xml")
    code = str(soup.code.text)
    if code == "0":
        zpid = str(soup.zpid.text)
        retInfo = [address, zipcode, zpid]
        return retInfo
    else:
        return "error"

# converts a select number of coordinates into addresses and inserts 
# into a listthe address/zipcode of those that match to a property
def findMatches(n):
	allCoords = genCoordinateList()
	print allCoords
	matchList = []
	counter = 0
	instream = open('../keys.csv','r')
	content = instream.readlines()
	instream.close()
	googleKey = content[2].split(",")[1].strip("\n")
	for coord in allCoords:
		latlngStr = str(coord[0]) + "," + str(coord[1])
		q = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
		q += latlngStr
		q += "&key=" + googleKey
		if counter % n == 0:
			u = urllib2.urlopen(q)
			response = u.read()
			d = json.loads(response)
			formatted_address = d["results"][0]["formatted_address"]
			addList.append(str(formatted_address))
			address = str(formatted_address.split(", ")[0])
			print address + "\n"
			zipcode = str(formatted_address.split(", ")[2][-5:])
			print zipcode + "\n"
			if isProperty(address, zipcode) != 'error':
				matchList.append(isProperty(address, zipcode))
				#print("\nsuccess!")
		counter += 1
	return matchList

# creates a dictionary of property info for a given address/zipcode
# assumes that given address/zipcode exists in zillow database
def genDictEntry(address, zipcode):
    infoDict = {}
    address = address.replace(" ", "+")
    instream = open('../keys.csv','r')
    content = instream.readlines()
    instream.close()
    zKey = content[1].split(",")[1].strip("\n")
    q = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?"
    q += "zws-id=" + zKey
    q += "&address=" + address
    q += "&citystatezip=" + zipcode
    u = urllib2.urlopen(q)
    response = u.read()
    soup = BeautifulSoup(response, "xml")
    infoDict['address'] = str(soup.street.text)
    infoDict['zipcode'] = str(soup.zipcode.text)
    infoDict['latitude'] = str(soup.latitude.text)
    infoDict['longitude'] = str(soup.longitude.text)
    infoDict['zestimatePrice'] = "$" + str(soup.amount.text)
    if str(soup.bathrooms) != 'None':
    	infoDict['bathrooms'] = str(soup.bathrooms.text)
    if str(soup.bedrooms) != 'None':
    	infoDict['bedrooms'] = str(soup.bedrooms.text)
    if str(soup.yearBuilt) != 'None':
    	infoDict['yearBuilt'] = str(soup.yearBuilt.text)
    if str(soup.useCode) != 'None':
    	infoDict['useCode'] = str(soup.useCode.text)
    if str(soup.finishedSqFt) != 'None':
    	infoDict['finishedSqFt'] = str(soup.finishedSqFt.text) + " sq feet"
    return infoDict

def genPropertyDictList(matchList):
   	propertyDictList = []
	for match in matchList:
		infoDict = genDictEntry(match[0], match[1])
		propertyDictList.append(infoDict)
	return propertyDictList

def centerCall(listOfCenters):
	ret = []
	for key in listOfCenters:
		dict = {}
		dict['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
		dict['lat'] = key[0]
		dict['lng'] = key[1]
		dict['infobox'] = "address"
		ret.append(dict)
	return ret

def makeMarkers(L1,L2):
	ret = []
	for key1 in L1:
		ret.append(key1)
	for key2 in L2:
		ret.append(key2)
	return ret

if __name__ == "__main__":
	#print isProperty("545 West 111th Street", "10025")
	#L = findMatches(4000)
	#genDictEntry("468 Riverside Dr APT 74", "10027")
	#genPropertyDictList(findMatches(1000))