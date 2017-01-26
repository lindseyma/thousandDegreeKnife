import urllib2, json, re, math, time, plot
from bs4 import BeautifulSoup
from pprint import pprint


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
            if isProperty(address, zipcode) != "error":
                zpidList.append(isProperty(address, zipcode))
                print("\nsuccess!")
        counter += 1
    print zpidList
    zpidNum = len(zpidList)
    addressNum = len(addressList)
    rate = (float)(zpidNum) / addressNum    
    print("# coords scanned = %d, # coords matched = %d, hit rate = %d\n")%(addressNum, zpidNum, rate)
    return zpidList


# assumes address comes with spaces, zip is string
# checks if address matches property
# returns zpid if true
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
        return zpid
    else:
        return "error"

# find address+zip for comparable properties
def getComparables(zpid):
    instream = open('../keys.csv','r')
    content = instream.readlines()
    instream.close()
    zKey = content[1].split(",")[1].strip("\n")
    q = "http://www.zillow.com/webservice/GetComps.htm?"
    q += "zws-id=" + zKey
    q += "&zpid=" + zpid
    q += "&count=" + "10"
    u = urllib2.urlopen(q)
    response = u.read()
    soup = BeautifulSoup(response, "xml")
    print(soup.prettify())
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
    print address_list
    print zip_list
    while pos < len(address_list):
        comp_list += [[address_list[pos], zip_list[pos]]]
        pos += 1
    print("\nlist of comparables = %s\n")%(str(comp_list))
    return comp_list

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
    infoDict['bathroomNum'] = str(soup.bathrooms.text)
    infoDict['bedroomNum'] = str(soup.bedrooms.text)
    infoDict['yearBuilt'] = str(soup.yearBuilt.text)
    infoDict['zestimatePrice'] = str(soup.amount.text)
    print(infoDict)

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

def genList():
    allProperties = []
    matchedProperties = genAddressHits()
    for match in matchedProperties:
        print match
        compList = getComparables(match)
        print compList
        for comp in compList:
            print comp[0]
            print comp[1]
            infoDict = genDictEntry(comp[0], comp[1])
            allProperties.append(infoDict)
    print allProperties
    return allProperties

    
if __name__ == "__main__":
    getComparables("48749425")
    #genDictEntry("440 Riverside Dr Apt 88", "10027")