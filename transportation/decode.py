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
year= 2018
month= 9
duplicate= -2
day_in_month=(31,28,31,30,31,30,31,31,30,31,30,31)
for month in range(3, 4):
	for day in range (1, day_in_month[month-1]+1):
		hour = -1
		if(datetime.date(2017, month, day).weekday()>4):
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
						num_t= -1
						dupli= False
						for i in dup:
							num_t+=1
							if(i== trip_id):
								dupli= True
								num=0
								if(len(en[num_t].stop_time_update)==0):
									break
								en_stop_ip= en[num_t].stop_time_update
								tt=t.stop_time_update
								if(len(en_stop_ip)< len(tt)):
									en[num_t]= t
									break
								while(en[num_t].stop_time_update[num].stop_id!= tt[0].stop_id):
									if(num+1 >= len(en[num_t].stop_time_update)):
										en[num_t] = t
										break
									num+=1
								for kk in tt:
									if(num< len(en[num_t].stop_time_update)-1):
										en[num_t].stop_time_update[num].departure.time= kk.departure.time
										num+=1
									elif(num== len(en[num_t].stop_time_update)-1):
										en[num_t].stop_time_update[num].arrival.time= kk.arrival.time
										num+=1
								break
						if(dupli== False):
							dup.append(trip_id)
							en.append(t)
							dupli= False
		for t in en:
			tt=t.stop_time_update
			tri= t.trip
			t_route_id= tri.route_id
			t_stop_id= tt[0].stop_id
			t_depart= tt[0].departure
			t_depart=datetime.datetime.fromtimestamp(
				int(t_depart.time)
			).strftime('%Y-%m-%d %H:%M:%S')
			year_num= int(t_depart[:4])
			month_num= int(t_depart[5:7])
			day_num= int(t_depart[8:10])
			hour_num= int(t_depart[11:13])
			if(year_num!= int(year) or month_num!= int(month) or day_num!= int(day)):
				continue
			nn= 1
			for i in tt:
				atime=i.departure.time
				if(nn == len(tt)):
					atime=i.arrival.time
				stop=i.stop_id
				atimenew=datetime.datetime.fromtimestamp(
					int(atime)
				).strftime('%Y-%m-%d %H:%M:%S')
				if(t_depart[11:13]=="23" or t_depart[8:10]!= day_str):
					break
				if((t.trip.route_id== '2' and (stop in target_stop_2n or stop in target_stop_2s)) or (t.trip.route_id== '1' and (stop in target_stop_1n or stop in target_stop_1s))):
					with open("b/"+t.trip.route_id+"/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+stop+".txt","a") as f:
						f.write(atimenew[11:16]+"   ")
				nn+=1