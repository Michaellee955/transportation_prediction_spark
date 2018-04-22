import os
from flask import Flask, request, abort, url_for, render_template, g, redirect, Response, session
from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import googlemaps
from datetime import datetime
import json
from tt import predict

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
    print(stop)
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

    now = datetime.now()
    directions_result = gmaps.directions(start,
                                         end,
                                         mode="transit",
                                         departure_time=now,
                                         alternatives=True)
    route_step=[]
    d=directions_result
    route_number=len(d)
    for i in range(route_number):
        route_info=d[i]['legs'][0]
        #print("route",i,"step number:",len(route_info['steps']),"\n")
        route_step.append(len(route_info['steps']))

    print("All route:",route_step)

    for i in range(len(route_step)):
        print("route",i+1,"info:","\n")
        for j in range(int(route_step[i])):
            transit_step=d[i]['legs'][0]['steps'][j]
            if transit_step['travel_mode']=='TRANSIT':
                transit_detail=transit_step['transit_details']
                line_object=transit_detail['line']
                if line_object['vehicle']['type']=='SUBWAY':

                    print("(1)route:",i+1,"(2)step:",j+1,"(3)stop:",transit_detail['departure_stop']['name'],"(4)line number:",line_object['short_name'],"(5)direction:",transit_detail['headsign'])
                else:
                    print("(1)route:",i+1,"(2)step:",j+1,"(3)stop:",transit_detail['departure_stop']['name'],"(4)line type:",line_object['vehicle']['type'])
                    route_step[i]=None
            else:

                print("(1)route:",i+1,"(2)step:",j+1,"Walk to transit stop")


    print("\n\nSubway route:",route_step)

    transit_array=[]

    for i in range(len(route_step)):
        if route_step[i]!=None:
            print("route",i+1,"info:","\n")
            transit_array_element=[]
            transit_dict_element={}
            for j in range(int(route_step[i])):
                transit_step=d[i]['legs'][0]['steps'][j]
                if transit_step['travel_mode']=='TRANSIT':
                    transit_detail=transit_step['transit_details']
                    line_object=transit_detail['line']
                    print("(1)route:",i+1,"(2)step:",j+1,"(3)stop:",transit_detail['departure_stop']['name'],"(4)line number:",line_object['short_name'],"(5)direction:",transit_detail['headsign'])
                    temp= dis[transit_detail['departure_stop']['name']]
                    if(line_object['short_name']=="1" and transit_detail['headsign']== "South Ferry"):
                        temp+= "S"
                    elif(line_object['short_name']=="1" and transit_detail['headsign']== "Van Cortlandt Park - 242 St"):
                        temp+= "N"
                    elif(line_object['short_name']=="2" and transit_detail['headsign']== "Wakefield - 241 St"):
                        temp+= "S"
                    elif(line_object['short_name']=="2" and transit_detail['headsign']== "Flatbush Av - Brooklyn College"):
                        temp+= "N"
                    transit_array_element.append(temp)
                else:

                    print("(1)route:",i+1,"(2)step:",j+1,"Walk to transit stop")
            transit_dict_element['Line']=line_object['short_name']
            transit_dict_element['Direction']=transit_detail['headsign']
            transit_dict_element['Stops']=transit_array_element
            transit_array.append(transit_dict_element)

    print(transit_array)


    transit_array_result=[]
    for item in transit_array:
        item=json.dumps(item)
        transit_array_result.append(item)
    transit_array_result=set(transit_array_result)

    result=[]
    for item in transit_array_result:
        item=json.loads(item)
        result.append(item)

    print("Result:",result)
    #return render_template('transit.html')
    return render_template("test.html",geocode=geocode)


if __name__ == "__main__":
    app.run(debug=True)
