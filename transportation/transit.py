api_key='AIzaSyDHswQXkT2wmHJXUeY6GvyTITMJF_iKC2k'
import googlemaps
from datetime import datetime

start='Columbia University'
end='Time Square'


gmaps = googlemaps.Client(key=api_key)

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
print(geocode_result[0])
print("************************")
print(geocode_result[0]['geometry']['location'])
print("************************")
s= str(geocode_result[0]['geometry']['location'])
print(s[1:-1])
# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("241 Street Station",
                                     "W 242nd St, Bronx, NY",
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

print(route_step)
route_step_subway=route_step

for i in range(len(route_step)):
	print("route",i+1,"info:","\n")
	for j in range(int(route_step[i])):
		transit_step=d[i]['legs'][0]['steps'][j]
		#print("route",i+1,"step",j,"travel mode",transit_step['travel_mode'],"\n")	
		#if 'transit_details' in transit_step.keys():
		if transit_step['travel_mode']=='TRANSIT':
			transit_detail=transit_step['transit_details']
			line_object=transit_detail['line']
			if line_object['vehicle']['type']=='SUBWAY':
				print("(1)route:",i+1,"(2)step:",j+1,"(3)stop:",transit_detail['departure_stop']['name'],"(4)line number:",line_object['short_name'],"(5)direction:",transit_detail['headsign'])
			else:
				print("(1)route:",i+1,"(2)step:",j+1,"(3)stop:",transit_detail['departure_stop']['name'],"(4)line type:",line_object['vehicle']['type'])
				route_step_subway[i]=None
		else:
			print("(1)route:",i+1,"(2)step:",j+1,"Walk to transit stop")
		'''if 'transit_details' in transit_step.keys():
			transit_object=transit_step['transit_details']
			if transit_object['line']['vehicle']['type']=='SUBWAY':
				print("route",i+1,"step",j,"departure_stop:",transit_object['departure_stop'],"line:",transit_object['line']['short_name'],"\n")	

'''
print(route_step_subway)
