import json
from pprint import pprint

with open('../data/policeprecincts.json') as data_file:    
    data = json.load(data_file)

#pprint(data)

new = []
def makeLatLng(string):
	string = string[12:]
	for x in string.split(", "):
			new.append(x.split(" "))
	return new
	
def trailing(li):
	li[0].pop(0)
	li[0][0]=li[0][0][3:]
	li[len(li)-1][1]=li[len(li)-1][1][:-3]
	
	
def popNew():
	x=0
	while x <= len(data["data"])-1:
		print len(data["data"])
		print (makeLatLng(data["data"][x][10]))[3]
		trailing(makeLatLng(data["data"][x][10]))
		x+=1
	

popNew()
print new [0]
print new [len(new)-1]
