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
	matchList = []
	matchNum = 0
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
			address = str(formatted_address.split(", ")[0])
			zipcode = str(formatted_address.split(", ")[2][-5:])
			if isProperty(address, zipcode) != 'error':
				matchList.append(isProperty(address, zipcode))
				matchNum += 1
				# print("success!\n")
			if matchNum > 60:
				break
		counter += 1
	# print matchList
	return matchList

def getComparables(zpid):
    instream = open('../keys.csv','r')
    content = instream.readlines()
    instream.close()
    zKey = content[1].split(",")[1].strip("\n")
    q = "http://www.zillow.com/webservice/GetComps.htm?"
    q += "zws-id=" + zKey
    q += "&zpid=" + zpid
    q += "&count=" + "3"
    u = urllib2.urlopen(q)
    response = u.read()
    soup = BeautifulSoup(response, "xml")
    address_box = soup.find_all("street")
    zip_box = soup.find_all("zipcode")
    pos = 0
    address_list = []
    zip_list = []
    comp_list = []
    for address in address_box:
        address_list += [str(address.text)]
    del address_list[0]
    for zipcode in zip_box:
        zip_list += [str(zipcode.text)]
    del zip_list[0]
    while pos < len(address_list):
        comp_list += [[address_list[pos], zip_list[pos]]]
        pos += 1
    return comp_list

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
    infoDict['detailsLink'] = str(soup.homedetails.text)
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
   	print matchList
	for match in matchList:
		infoDict = genDictEntry(match[0], match[1])
		propertyDictList.append(infoDict)
		# compList = getComparables(match[2])
		# for comparable in compList:
		# 	print("comp address: %s\n")%(comparable[0])
		# 	print("comp zip: %s\n")%(comparable[1])
		# 	infoDict = genDictEntry(comparable[0], comparable[1])
		# 	propertyDictList.append(infoDict)
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


# functions for site scraping
'''
def getDetailLink(zpid):
    instream = open('../keys.csv','r')
    content = instream.readlines()
    instream.close()
    zKey = content[1].split(",")[1].strip("\n")
    q = "http://www.zillow.com/webservice/GetZestimate.htm?"
    q += "zws-id=" + zKey
    q += "&zpid=" + zpid
    u = urllib2.urlopen(q)
    response = u.read()
    soup = BeautifulSoup(response, "xml")
    link = str(soup.homedetails.text)
    latitude = str(soup.latitude.text)
    longitude = str(soup.longitude.text)
    retInfo = [link, latitude, longitude]
    print retInfo
    return retInfo
'''

'''
# scrape data off of the property's info page and package as dict
def getPropertyInfo(infoList):
    link = infoList[0]
    u = urllib2.urlopen(link)
    response = u.read()
    soup = BeautifulSoup(response, "html5lib")
    infoDict = {}
    infoDict['address'] = str(soup.title.text).split("|")[0].strip()
    infoDict['latitude'] = infoList[1]
    infoDict['longitude'] = infoList[2]
    #infoDict['image1'] = 'url'
    print "\n" + str(soup.title.text).split("|")[0].strip() + "\n"
    print "\n" + str(soup.find_all("meta content")) + "\n\n\n"
    # for tag in soup.find("meta", name="ROBOTS"):
    #     print tag["content"]
    print soup
    #return infoDict
'''





if __name__ == "__main__":
	#print isProperty("545 West 111th Street", "10025")
	#L = findMatches(4000)
	#genDictEntry("468 Riverside Dr APT 74", "10027")
	#print findMatches(1000)
	print genPropertyDictList(findMatches(1000))
