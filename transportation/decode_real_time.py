import datetime
import os
import sys
import datetime
import numpy as np
import time
import requests
from astropy.table import Table, Column
from google.transit import gtfs_realtime_pb2


target_stop_1s= ["101S", "103S", "112S", "115S", "119S", "120S", "124S", "127S", "137S", "142S"]
target_stop_1n= ["101N", "103N", "112N", "115N", "119N", "120N", "124N", "127N", "137N", "142N"]
target_stop_2s= ["201S", "213S", "221S", "224S", "120S", "127S", "132S", "137S", "235S", "239S", "247S"]
target_stop_2n= ["201N", "213N", "221N", "224N", "120N", "127N", "132N", "137N", "235N", "239N", "247N"]
#path2='https://datamine-history.s3.amazonaws.com/gtfs-2014-09-17-09-36'
#path2='https://datamine-history.s3.amazonaws.com/gtfs-2014-09-17-09-36'
arry=[]
aa= False
feed = gtfs_realtime_pb2.FeedMessage()
dup = []
dupli = False
en=[]
path='https://datamine-history.s3.amazonaws.com/gtfs'
duplicate= -2
while(1):
	time_now= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	year= time_now[:4]
	month= time_now[5:7]
	day= time_now[8:10]
	hour= time_now[11:13]
	minute= time_now[14:16]
	if(minute== "00"):
		minute_str= "56"
		hour= str(int(hour)-1)
	else:
		while (int(minute)%5!= 1):
			minute= str(int(minute)-1)
	tem= path+'-'+ str(year) +'-'+ month+'-'+day+'-'+hour+'-'+minute
	print(tem)
	response = requests.get(tem)
	try:
		feed.ParseFromString(response.content)
	except:
		continue
	all_num=0
	for entity in feed.entity:
		if entity.HasField('trip_update'):
			t=entity.trip_update
			tri= t.trip
			if(tri.route_id==""):
				continue
			trip_id= tri.trip_id
			tt= t.stop_time_update
			tri= t.trip
			stop=tt[0].stop_id
			t_route_id= tri.route_id
			t_stop_id= tt[0].stop_id
			if(len(tt)==1):
				t_depart=datetime.datetime.fromtimestamp(
					int(tt[0].arrival.time)
				).strftime('%Y-%m-%d %H:%M:%S')
			else:
				t_depart=datetime.datetime.fromtimestamp(
					int(tt[0].departure.time)
				).strftime('%Y-%m-%d %H:%M:%S')
			if(t_depart[11:13]=="23" or t_depart[8:10]!= day):
				continue
			if((t.trip.route_id== '2' and (stop in target_stop_2n or stop in target_stop_2s)) or (t.trip.route_id== '1' and (stop in target_stop_1n or stop in target_stop_1s))):
				with open("b/"+str(int(t.trip.route_id)+4)+"/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+stop+".txt","a") as f:
					f.write(t_depart[11:16]+"   ")
	time.sleep(300)