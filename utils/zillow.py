from bs4 import BeautifulSoup
from pprint import pprint

# assumes address comes with spaces, zip is string
# checks if address matches property
# returns zpid if true

allList = [['40.537131', '-74.21224'], ['40.588500', '-74.10106'], ['40.615816', '-74.14591'], ['40.627391', '-74.02601'], ['40.598213', '-73.98086'], ['40.578595', '-73.96115'], ['40.569997', '-73.86318'], ['40.589119', '-73.92673'], ['40.620668', '-73.90876'], ['40.637409', '-73.90660'], ['40.641621', '-73.95181'], ['40.633921', '-74.00582'], ['40.665659', '-73.97677'], ['40.683076', '-73.99081'], ['40.659893', '-73.94622'], ['40.643586', '-73.92688'], ['40.633832', '73.891449'], ['40.675667', '-73.92772'], ['40.679465', '-73.95082'], ['40.697429', '-73.98822'], ['40.770561', '-73.96410'], ['40.686358', '-73.93162'], ['40.675927', '-73.89760'], ['40.657448', '-73.88082'], ['40.718998', '-74.00812'], ['40.724668', '-73.98122'], ['40.732459', '-74.00126'], ['40.733236', '-73.98542'], ['40.747968', '-74.00225'], ['40.747410', '-73.97440'], ['40.763252', '-73.97612'], ['40.756329', '-73.96564'], ['40.768938', '-73.95605'], ['40.782705', '-3.980223'], ['40.794523', '-73.96493'], ['40.803364', '-73.94709'], ['40.799535', '-73.94065'], ['0.824367,', '-73.94677'], ['40.846217', '73.939399'], ['40.748839', '-73.91489'], ['40.776432', '-73.90735'], ['40.755023', '-73.87627'], ['40.733468', '-73.85961'], ['39.817271', '-105.0612'], ['40.724030', '-73.84484'], ['40.731028', '-72.79958'], [40.811756, -73.919961], [40.830534, -73.927918], [40.824030, -73.890192], [40.829646, -73.915838], [40.849492, -73.904476], [40.847043, -73.891285], [40.815615, -73.862858], [40.844889, -73.854286], [40.836148, -73.818968], [40.866769, -73.853500], [40.877806, -73.875006], ['40.904549', '-73.898656']]

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