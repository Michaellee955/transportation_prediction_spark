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
import copy
from stack import StackingAveragedModels

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'LargeData2018SpringGroup10'
api_key='AIzaSyDHswQXkT2wmHJXUeY6GvyTITMJF_iKC2k'
GoogleMaps(app,key=api_key)

dis={"168 Street Station": "112", "Van Cortlandt Park - 242 St": "101", "238th Street Station": "103",
"137 St - City College": "115", "103 St": "119", "96 St": "120", "66 St - Lincoln Center Subway Station": "124",
"Times Square-42 Street": "127", "Chambers St Subway Station": "137", "South Ferry": "142", "59 St - Columbus Circle Station": "125",
"241 Street Station": "201", "E 180 St": "213", "3 Av - 149 St": "221", "135 St": "224", "14 St": "132", "Atlantic Av-Barclays Ctr": "235",
"Franklin Av": "239", "Flatbush Av - Brooklyn College": "247"}

dis_value={"112": "168 Street Station", "101": "Van Cortlandt Park - 242 St", "103": "238th Street Station",
"115": "137 St - City College", "119": "103 St", "120": "96 St", "124": "66 St - Lincoln Center Subway Station",
"127": "Times Square-42 Street", "137": "Chambers St Subway Station", "142": "South Ferry", "125": "59 St - Columbus Circle Station",
"201": "241 Street Station", "213": "E 180 St", "221": "3 Av - 149 St", "224": "135 St", "132": "14 St", "235": "Atlantic Av-Barclays Ctr",
"239": "Franklin Av", "247": "Flatbush Av - Brooklyn College"}

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
    global dis_value
    stop=request.form['option']
    l=stop[:1]
    d=stop[6:8]
    s=stop[2:5]

    delay = predict(l,s+d)

    s=dis_value[s]
    message={}
    message['line']=l
    message['direction']=d
    message['stop']=s
    message['delay']=form(float(delay))

    return render_template("test.html", m=message)


@app.route("/transit", methods=['POST'])
def transit():
    global dis
    global dis_value
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
        delay_copy=copy.deepcopy(delay)
        delay_mid=[]
        rec=[]
        for item in delay_copy:
            item['Route']=None
            item['arrival']=None
            if item not in delay_mid:
                delay_mid.append(item)
                rec.append(True)
            else:
                rec.append(False)
        delay_display=[]
        for i in range(len(rec)):
            if rec[i]==True:
                delay_display.append(delay[i])
        print("\n","Delay Display",delay_display)
        delay_display_result=[]
        for item in delay_display:
            arrival_time=item['arrival']
            delay_time=item['delay']
            if(len(arrival_time)== 6):
                arrival_time_num= int(arrival_time[:1])* 3600 + int(arrival_time[2:4])* 60
            elif(len(arrival_time)== 7):
                arrival_time_num= int(arrival_time[:2])* 3600 + int(arrival_time[3:5])* 60
            arrival_time_num+= delay_time
            hour_num= int(arrival_time_num/3600)
            minute_num= int((arrival_time_num- 3600 * hour_num)/ 60)
            if(minute_num< 10):
                minute_num_str= "0"+ str(minute_num)
            else:
                minute_num_str= str(minute_num)
            second_num= int(arrival_time_num- 3600* hour_num- 60* minute_num)
            if(second_num< 10):
                second_num_str= "0"+ str(second_num)
            else:
                second_num_str= str(second_num)
            arrival_time= str(hour_num)+":"+ minute_num_str+":"+ second_num_str+ arrival_time[-2:]
            item['arrival_time']=arrival_time
            temp=[]
            for i in range(len(item['Stops'])):
                temp.append(dis_value[item['Stops'][i][:3]])
            item['Stops']=temp
            delay_display_result.append(item)
        d=delay_display_result
        print("\n","Delay Display Result",delay_display_result)
        return render_template("testold.html",geocode=geocode,d=d)
    else:
        e="There is no available predicted delay, sorry."
        return render_template("testold.html",geocode=geocode,e=e)

def form(delay):
    mag = 30.0
    d = round(delay*60,2)
    result = 0
    if d>0:
        result = d+mag
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
