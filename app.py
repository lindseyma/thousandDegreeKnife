from flask import Flask, render_template, request
from utils import listparse, plot, APIReader
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


import json


app = Flask(__name__)
GoogleMaps(app, key=APIReader.getKey("Google_Maps"))


@app.route("/")
def root():
    NYTKey = APIReader.getKey("NTY_topstoriesV2")
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=40.7128, 
        lng=-74.0059,
        style="width:100%;height:500px;",
        markers=plot.crimeCall()
    )
    #center property lat long in each borough and make calls to plot the properties
    return render_template('map.html', mymap=mymap, populateLatLng = "listparse.main()", crimeList = len(plot.crimeCall()), crime = plot.crimeCall(), NYTKey=NYTKey)
	
@app.route("/listing/")
def listing():
		# in rendering, show house details for the selected house
		#zip, street, lat long, amt, contact, photos
    return render_template("house.html", house="")

if __name__ == '__main__':
    app.debug = True
    app.run()
