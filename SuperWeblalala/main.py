import os
from flask import Flask, request, abort, url_for, render_template, g, redirect, Response, session
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import googlemaps
from datetime import datetime
import json
from tt import predict
from parse import parseStop
from stack import StackingAveragedModels

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'LargeData2018SpringGroup10'
api_key='AIzaSyDHswQXkT2wmHJXUeY6GvyTITMJF_iKC2k'
GoogleMaps(app,key=api_key)


@app.route("/")
def index():

    return render_template('index.html')

@app.route('/transit')
def another():
    return render_template("transit.html")

@app.route('/test')
def another2():
    #{lat: 37.77, lng: -122.447}
    #{lat: 37.768, lng: -122.511}
    lat1=37.77
    lon1=-122.447
    lat2=37.768
    lon2=-122.511
    geocode=lat1,lon1,lat2,lon2
    return render_template("test.html",geocode=geocode)

@app.route("/test", methods=['POST'])
def test():
    global api_key
    stop=request.form['option']
    message=[]
    l=stop[:1]
    d=stop[6:8]
    s=stop[2:5]

    delay = predict(l,s,d)

    message={}
    message['line']=l
    message['direction']=d
    message['stop']=s
    message['delay']=delay

    return render_template("test.html", m=message)


@app.route("/transit", methods=['POST'])
def transit():
    global dis
    global api_key
    start=request.form['start']
    end=request.form['end']
    gmaps = googlemaps.Client(key=api_key)
    locations=gmaps.geocode(start)
    locatione=gmaps.geocode(end)
    ds=locations[0]
    de=locatione[0]
    lat1=ds['geometry']['location']['lat']
    lon1=ds['geometry']['location']['lng']
    lat2=de['geometry']['location']['lat']
    lon2=de['geometry']['location']['lng']
    geocode=lat1,lon1,lat2,lon2
    #return render_template("test.html",geocode=geocode)
    result=parseStop(gmaps,start,end)
    if result !=[]:
        delay=predictQuery(result)
        print(delay)
    else:
        print("No....")
    return render_template("testold.html",geocode=geocode)

def predictQuery(result):
    print("lalalala")
    delay={}
    return delay

if __name__ == "__main__":
    app.run(debug=True)
