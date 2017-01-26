import json, re, math, time
from pprint import pprint
import plot

# with open('../data/policeprecincts.json') as data_file:    
#     data = json.load(data_file)

with open('data/policeprecincts.json') as data_file:    
     data = json.load(data_file)

#pprint(data)

#data = "MULTIPOLYGON (((-74.0438776157395 40.69018767637665, -74.0435059601254 40.68968735963635, -74.04273533826982 40.69005019142044, -74.04278433380006 40.69012097669115, -74.04270428426766 40.690155204644306, -74.04255372037308 40.6899627592896, -74.0426392937119 40.68992817641333, -74.0426938081918 40.689997259107216, -74.04346752310265 40.68963699010347, -74.04351637245855 40.68919103374234, -74.04364078627412 40.68876655957014, -74.04397458556184 40.68858240705591, -74.0443852177728 40.688516178402686, -74.04478399040363 40.68859566011588, -74.04627539003668 40.689327425896714, -74.04680284898575 40.68995325626601, -74.04747651462345 40.68961136999828, -74.04772962763064 40.68991531846602, -74.04758571924786 40.68998250682616, -74.04743126123475 40.68980388996831, -74.04689205500591 40.69005909832262, -74.04720029366251 40.69042481562375, -74.04711050698607 40.69047041285008, -74.04711582042361 40.6906558061182, -74.04718321412064 40.69074735504909, -74.04719492513735 40.690763263848176, -74.04721324571446 40.69079048740705, -74.04722568429027 40.690819572604845, -74.04723192827481 40.69084978852888, -74.04723182074775 40.69088037585023, -74.04722536440258 40.690910565905725, -74.04721272147984 40.69093960001451, -74.04719420969079 40.69096674854391, -74.04717029423398 40.690991329245335, -74.04714090993608 40.69101051668724, -74.04710814004659 40.69102620867961, -74.04707269621697 40.69103806444433, -74.04703534816912 40.69104582651328, -74.04699690697936 40.69104932631987, -74.04617167065449 40.69109798148633, -74.04614707208631 40.6911226455306, -74.04609551065103 40.691120063047265, -74.04604442455498 40.69111415215903, -74.04599418395532 40.69110495569473, -74.04592592732845 40.69108260333731, -74.04586027361351 40.69105611608104, -74.04460616482923 40.69057348495081, -74.0438776157395 40.69018767637665)),  ((-74.03995040788514 40.70089063064273, -74.03945262913307 40.70053315982373, -74.03938278052782 40.70057769405894, -74.03771124796636 40.699344040347725, -74.03809786214774 40.6990395052442, -74.03822954445361 40.69836859119513, -74.03900043878028 40.69836989039101, -74.0393403767015 40.69811551483597, -74.03993272132986 40.69854442279366, -74.0402555501724 40.69880482330755, -74.04124261832222 40.699536741434855, -74.04174768868015 40.699147863566644, -74.03991248872623 40.6977020403984, -74.04166051914841 40.69645297163976, -74.04367371164746 40.69802040433034, -74.04363686145162 40.698048232698525, -74.04365651062231 40.69806409108789, -74.04270395810691 40.69880060008409, -74.04296505227546 40.69899936232474, -74.04109861171034 40.700492943389875, -74.04080080646241 40.70026854992651, -74.04031250973499 40.70062574868964, -74.0403910438396 40.70068737620885, -74.04041179161338 40.70067848411861, -74.04053637732214 40.70078209477503, -74.04048062485343 40.70082061467004, -74.04034955264609 40.70071601865484, -74.0403651116708 40.700704167347894, -74.04028808803947 40.700643613467136, -74.03995040788514 40.70089063064273)))"
#data["data"][x][10]

#makes list from string
def makeLatLng(s):
	rowList = []
	for x in re.split(r'[()]', s):
		if len(x) > 3:
			for y in x.split(", "):
				rowList.append(y.split(" "))
	return rowList

#helper to remove ((( )))
def trailing(li):
	li[0].pop(0)
	li[0][0]=li[0][0][3:]
	li[len(li)-1][1]=li[len(li)-1][1][:-3]

allList = []
	
#generates list of 
def genBorder():
	x=0
	#print("the weird number is %d\n\n\n")%(len(data["data"]) - 1)
	while x < len(data["data"]):
		data["data"][x][10] = data["data"][x][10][13:] #cut out multipolygon
		allList.append(makeLatLng(data["data"][x][10]))
		x+=1
	#print allList
	
def genCenter():
	borderList = allList
	borderListv2 = []
	centerList = []
	rowNum = 0
	#print("len(borderList) = %s\n\n")%(len(borderList))
	for row in borderList:
		#print("row %d length = %s")%(rowNum + 1, len(row))
		#time.sleep(0.5)
		pos = 0;
		initLat = (float)(row[0][1])
		initLon = (float)(row[0][0])
		singleArea = [[initLat, initLon]]
		for coordinate in row:
			#print("\n\n\nprinting latlong\n")
			lat = (float)(coordinate[1]) 
			lon = (float)(coordinate[0])
			#print [lat, lon]
			if [lat, lon] == singleArea[0] and len(singleArea) > 1 and pos < len(row) - 1: #end of area, not of row 
				#print("\nhit same coordinate\n")
				del singleArea[0]
				borderListv2.append(singleArea)
				#print("\n\nprinting final single area, not end of row\n\n")
				#print str(singleArea) + "\t" + str(len(singleArea))
				nextLat = (float)(row[pos+1][1])
				nextLon = (float)(row[pos+1][0])
				#print("\n\n\nprinting first latlong of next area\n")
				singleArea = [[nextLat, nextLon]]
				#print singleArea
				#time.sleep(8)
			elif [lat, lon] == singleArea[0] and len(singleArea) > 1 and rowNum == len(borderList): #end of area and row 
				#print("\nhit same coordinate\n")
				del singleArea[0]
				borderListv2.append(singleArea)
				#print("\n\nprinting final single area, end of row AND entire list\n\n")
				#print str(singleArea) + "\t" + str(len(singleArea))
			else:
				#print("\nadding coordinate\n")
				singleArea += [[lat, lon]]
				#print str(singleArea) + "\t" + str(len(singleArea))
				#time.sleep(0.1)
			pos += 1
		rowNum += 1
	
	#print("\n\ndone!\n")
	
	for neighborhood in borderListv2:
		centerLat = 0
		centerLon = 0
		#print borderListv2[len(borderListv2)-1]
		for coordinate in neighborhood:
			centerLat += coordinate[0]
			centerLon += coordinate[1]
		centerLat = centerLat / len(neighborhood)
		centerLon = centerLon / len(neighborhood)
		centerList.append([centerLat, centerLon])
	return centerList
	#print "\ndone2!\n"
	#print("\n\nprinting borderListv2\n\n")
	#print borderListv2

def centerCall(listOfCenters):

	ret = []
	for key in listOfCenters:

		dict = {}
		dict['icon'] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
		dict['lat'] = key[0]
		dict['lng'] = key[1]
		dict['infobox'] = '<a href="listing/">440 Riverside Dr APT 88, New York, NY 10027</a>'
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
		#print key1
	for key2 in L2:
		#print key2
	return True
'''


	
	
	
def main():
	#li = makeLatLng(data)
	#new[len(li)-1][1]=new[len(li)-1][1][:-3]
	#popNew()
	#print "["+jsLatLng()+"]"
	
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

genBorder()
#print genCenter()
#print makeMarkers(plot.crimeCall(),centerCall(genCenter()))

centerlist=[[40.8089, -73.9673697]]
#print centerCall(centerlist)
#L = [[1, 1], [2, 2]]
#print L[0]