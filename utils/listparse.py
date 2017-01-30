import urllib2, json, re, math, time, plot
import zillow
from pprint import pprint

# with open('../data/policeprecincts.json') as data_file:    
#     data = json.load(data_file)

with open('../data/policeprecincts.json') as data_file:    
     data = json.load(data_file)


# converts string of row to list of coordinates
def makeLatLng(s):
	rowList = []
	for x in re.split(r'[()]', s):
		if len(x) > 3:
			for y in x.split(", "):
				rowList.append(y.split(" "))
	return rowList

allList = []
	
# generates list of rows
def genBorder():
	x=0
	while x < len(data["data"]):
		data["data"][x][10] = data["data"][x][10][13:] #cut out multipolygon
		allList.append(makeLatLng(data["data"][x][10]))
		x+=1
	# print allList
	
# note: total number of coordinates ~90k
def genCoordList():
	borderList = allList
	borderListv2 = []
	coordList = []
	rowNum = 0
	for row in borderList:
		for coordinate in row:
			lat = (float)(coordinate[1]) 
			lon = (float)(coordinate[0])
			coordList.append([lat, lon])
	return coordList

# scans coords to find any that match a property in zillow database
# adds matches to a list and returns
def genAddressHits():
	coordList = genCoordList()
	zpidList = []
	addressList = []
	instream = open('../keys.csv','r')
	content = instream.readlines()
	instream.close()
	googleKey = content[2].split(",")[1].strip("\n")
	print("google key is: %s\n")%(googleKey)
	counter = 0
	for coord in coordList:
		latlngStr = str(coord[0]) + "," + str(coord[1])
		print("latlngStr is: %s\n")%(latlngStr)
		q = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
		q += latlngStr
		q += "&key=" + googleKey
		if counter % 100 == 0: 
			u = urllib2.urlopen(q)
			response = u.read()
			d = json.loads(response)
			formatted_address = d["results"][0]["formatted_address"]
			print str(formatted_address) + "\n"
			addressList.append(str(formatted_address))
			address = str(formatted_address.split(", ")[0])
			# print address + "\n"
			zipcode = str(formatted_address.split(", ")[2][-5:])
			# print zipcode + "\n"
			if zillow.isProperty(address, zipcode) != "error":
				zpidList.append(zillow.isProperty(address, zipcode))
				print("\nsuccess!")
		counter += 1
	print zpidList
	zpidNum = len(zpidList)
	addressNum = len(addressList)
	#rate = (float)(zpidNum) / addressNum	
	print("# coords scanned = %d, # coords matched = %d")%(addressNum, zpidNum)
	pos = 0
	while pos < len(zpidList):
		if zpidList[pos] == 'error':
			del zpidList[pos]
			pos += 1
	return zpidList


def centerCall(listOfCenters):
	ret = []
	for key in listOfCenters:
		dict = {}
		dict['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
		dict['lat'] = key[0]
		dict['lng'] = key[1]
		dict['infobox'] = '<a href="listing/%s">%s</a>' %(key[2],key[2])
		ret.append(dict)
	return ret

def makeMarkers(L1,L2):
	ret = []
	for key1 in L1:
		ret.append(key1)
	for key2 in L2:
		ret.append(key2)
	return ret
'''
def makeMarkers(L1,L2):
	ret = []
	for key1 in L1:
		print key1
	for key2 in L2:
		print key2
	return True
'''


	
	
	
def main():
	#li = makeLatLng(data)
	#new[len(li)-1][1]=new[len(li)-1][1][:-3]
	#popNew()
	print "["+jsLatLng()+"]"
	
	return "["+jsLatLng()+"]"
	
#main()
#print data
#popNew()
x = 0

'''
print data["data"][76][10]
print makeLatLng( data["data"][76][10] )
print x
'''

#genBorder()
#print genCenter()
#print makeMarkers(plot.crimeCall(),centerCall(genCenter()))
#genAddressHits()

