from flask import Flask, render_template, request
from utils import listparse
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


import json


app = Flask(__name__)
GoogleMaps(app, key="AIzaSyANxJ7nnBsOv8PTwcEQB8cNG_lsLpsII50")


@app.route("/")
def root():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=40.7128, 
        lng=-74.0059,
        style="width:100%;height:500px;"
    )
    return render_template('map.html', mymap=mymap, populateLatLng = listparse.main())
	
@app.route("/listing/")
def listing():
    return render_template("house.html", house="")

if __name__ == '__main__':
    app.debug = True
    app.run()
