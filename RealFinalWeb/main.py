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
    l=stop[:1]
    d=stop[6:8]
    s=stop[2:5]

    delay = predict(l,s+d)

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
        print("\n","Delay:",delay)
        delay_display=[]
        for item in delay:
            item['Route']=None
            item=json.dumps(item)
            delay_display.append(item)
        delay_display=set(delay_display)

        delay_display_result=[]
        for item in delay_display:
            item=json.loads(item)
            delay_display_result.append(item)
        print("\n","Delay Display",delay_display_result)
        d=delay_display_result
        return render_template("testold.html",geocode=geocode,d=d)
    else:
        e="There is no available predicted delay, sorry."
        return render_template("testold.html",geocode=geocode,e=e)

def form(delay):
    mag = 30.0
    d = round(delay*60,2)
    result = 0
    if d>0:
        result = mag
    elif d<0:
        result = d-mag

    return result

def predictQuery(result):
    result_list = []
    for item in result:
        lines = item['Line']
        stops = item['Stops']
        delay_sum = 0
        for i in range(len(lines)):
            delay = 0
            if 'S' in stops[i] or 'N' in stops[i]:
                if lines[i]=='1' or lines[i]=='2':
                    delay = list(predict(lines[i],stops[i]))[0]
            delay_sum += form(delay)
        item['delay'] = delay_sum
        result_list.append(item)
    return result_list

if __name__ == "__main__":
    app.run(debug=True)
