from flask import Flask, render_template, request
from utils import map

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("map.html")
	
@app.route("/listing/")
def listing():
    return render_template("house.html", house="")

if __name__ == '__main__':
    app.debug = True
    app.run()
