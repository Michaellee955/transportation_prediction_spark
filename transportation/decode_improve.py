import datetime
import os
import sys
import datetime
import numpy as np
import requests
from astropy.table import Table, Column
from google.transit import gtfs_realtime_pb2


target_stop_1s= ["101S", "103S", "112S", "115S", "119S", "120S", "124S", "127S", "137S", "142S"]
target_stop_1n= ["142N", "137N", "127N", "125N", "120N", "115N", "112N", "104N", "103N", "101N"]
target_stop_2s= ["201S", "213S", "221S", "224S", "120S", "127S", "132S", "137S", "235S", "239S", "247S"]
target_stop_2n= ["247N","239N","235N","137N","132N","127N","120N","224N","221N","213N","201N"]
#path2='https://datamine-history.s3.amazonaws.com/gtfs-2014-09-17-09-36'
#path2='https://datamine-history.s3.amazonaws.com/gtfs-2014-09-17-09-36'
arry=[]
aa= False
feed = gtfs_realtime_pb2.FeedMessage()
dup = []
dupli = False
en=[]
path='https://datamine-history.s3.amazonaws.com/gtfs'
year= 2017
month= 9
duplicate= -2
day_in_month=(31,28,31,30,31,30,31,31,30,31,30,31)
for day in range (1, 15):
	hour = -1
	if(datetime.date(2017, 9, day).weekday()>4):
		continue
	for k in range (24):
		hour+= 1
		minute= -4
		for j in range (12):
			minute+= 5
			if(month<10):
				month_str= '0'+ str(month)
			else:
				month_str= str(month)
			if(day<10):
				day_str= '0'+ str(day)
			else:
				day_str= str(day)
			if(hour<10):
				hour_str= '0'+ str(hour)
			else:
				hour_str= str(hour)
			if(minute<10):
				minute_str= '0'+ str(minute)
			else:
				minute_str= str(minute)
			tem= path+'-'+ str(year) +'-'+ month_str+'-'+day_str+'-'+hour_str+'-'+minute_str
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
					if(t_depart[11:13]=="23" or t_depart[8:10]!= day_str):
						continue
					if((t.trip.route_id== '2' and (stop in target_stop_2n or stop in target_stop_2s)) or (t.trip.route_id== '1' and (stop in target_stop_1n or stop in target_stop_1s))):
						with open("b/"+str(int(t.trip.route_id)+2)+"/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+stop+".txt","a") as f:
							f.write(t_depart[11:16]+"   ")