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
    li = [['40.80891', '-73.965217',"3 Claremont Ave, New York, NY 10027, USA"], ['40.803096', '-73.964805',"510 W 110th St, New York, NY 10025, USA"], ['40.803207', '-73.964866',"504 W 110th St, New York, NY 10025, USA"], ['40.803428', '-73.965591',"520 Cathedral Pkwy, New York, NY 10025, USA"], ['40.80373', '-73.964225',"504 W 111th St, New York, NY 10025, USA"]]

    centerlist=[[40.808905, -73.965183,"440 Riverside Dr APT 88, New York, NY 10027"]]
    for x in li:
        centerlist.append([float(x[0]),float(x[1]),x[2]])
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
