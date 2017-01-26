from bs4 import BeautifulSoup
from pprint import pprint

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