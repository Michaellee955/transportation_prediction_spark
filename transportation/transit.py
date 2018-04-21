api_key='AIzaSyDHswQXkT2wmHJXUeY6GvyTITMJF_iKC2k'
import googlemaps
from datetime import datetime
import json

dis={"168 Street Station": "112", "Van Cortlandt Park - 242 St": "101", "238th Street Station": "103", 
"137 St - City College": "115", "103 St": "119", "96 St": "120", "66 St - Lincoln Center Subway Station": "124",
"Times Square-42 Street": "127", "Chambers St Subway Station": "137", "South Ferry": "142", "59 St - Columbus Circle Station": "125",
"241 Street Station": "201", "E 180 St": "213", "3 Av - 149 St": "221", "135 St": "224", "14 St": "132", "Atlantic Av-Barclays Ctr": "235",
"Franklin Av": "239", "Flatbush Av - Brooklyn College": "247"}

start="103 St"
end="Flushing"


gmaps = googlemaps.Client(key=api_key)

locations=gmaps.geocode(start)
locatione=gmaps.geocode(end)
ds=locations[0]
de=locatione[0]
lat1=ds['geometry']['location']['lat']
lon1=ds['geometry']['location']['lng']
lat2=de['geometry']['location']['lat']
lon2=de['geometry']['location']['lng']

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

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