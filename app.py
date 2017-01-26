from flask import Flask, render_template, request
from utils import listparse, plot, APIReader, news
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


import json


app = Flask(__name__)
GoogleMaps(app, key=APIReader.getKey("Google_Maps"))


@app.route("/")
def root():
    # creating a map in the view
    li = [['40.80891', '-73.965217'], ['40.803096', '-73.964805'], ['40.803207', '-73.964866'], ['40.803428', '-73.965591'], ['40.80373', '-73.964225'], ['40.80437', '-73.965769'], ['40.80384', '-73.964996'], ['40.801696', '-73.967453'], ['40.802411', '-73.966224'], ['40.802814', '-73.966705'], ['40.803253', '-73.965827'], ['40.804389', '-73.967964'], ['40.803417', '-73.967765'], ['40.803981', '-73.965545'], ['40.802411', '-73.966224'], ['40.805563', '-73.959818'], ['40.803745', '-73.964233'], ['40.806159', '-73.966064'], ['40.8034', '-73.9678'], ['40.804199', '-73.966056'], ['40.804199', '-73.966056'], ['40.804199', '-73.966056'], ['40.806159', '-73.966064'], ['40.811868', '-73.959116'], ['40.802411', '-73.966224'], ['40.81352', '-73.959116']]

    centerlist=[[40.808905, -73.965183]]
    for x in li:
        centerlist.append([float(x[0]),float(x[1])])
    L2=listparse.centerCall(centerlist)

    mymap = Map(
        identifier="view-side",
        lat=40.808905,
        lng=-73.965183,
        zoom=16,
        style="width:100%;height:500px;",
        markers=listparse.makeMarkers(plot.crimeCall(),L2)
    )

    #center property lat long in each borough and make calls to plot the properties
    return render_template('map.html', mymap=mymap, populateLatLng = "listparse.main()", crimeList = len(plot.crimeCall()), crime = plot.crimeCall())
	
@app.route("/listing/<address>")
def listing(address):
		try:
			housesList = findHouses.genList()
			for i in houseList:
					if i['address'] == address:
							return render_template("house.html", Address=address, Price=i['price'], Beds=i['beds'], Bathrooms=i['bathrooms'], latitude=i['latitude'], longitude=i['longitude'], facts=i['facts'])
		except:
			return render_template("house.html", Address=address, Price="$", Beds="Num of Beds", Bathrooms="Num of Bathrooms", latitude="latitude", longitude="longitude", facts="facts")
    
@app.route("/news/")
def getNews():
    return news.newsCall(APIReader.getKey("NYT_topstoriesV2"))

if __name__ == '__main__':
    app.debug = True
    app.run()
