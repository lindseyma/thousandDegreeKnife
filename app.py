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
    centerlist=[[40.8089, -73.9673697]]
    L2=listparse.centerCall(centerlist)

    mymap = Map(
        identifier="view-side",
        lat=40.8089,
        lng=-73.9673697,
        style="width:100%;height:500px;",
        markers=listparse.makeMarkers(plot.crimeCall(),L2)
    )

    #center property lat long in each borough and make calls to plot the properties
    return render_template('map.html', mymap=mymap, populateLatLng = "listparse.main()", crimeList = len(plot.crimeCall()), crime = plot.crimeCall())
	
@app.route("/listing/")
def listing():
		# in rendering, show house details for the selected house
		#zip, street, lat long, amt, contact, photos
    return render_template("house.html", house="")
    
@app.route("/news/")
def getNews():
    return news.newsCall(APIReader.getKey("NYT_topstoriesV2"))

if __name__ == '__main__':
    app.debug = True
    app.run()
