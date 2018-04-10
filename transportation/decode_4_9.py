import datetime
import os
import sys
import datetime
import numpy as np
import requests
from astropy.table import Table, Column
from google.transit import gtfs_realtime_pb2

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
for day in range (8, 15):
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
					num_t= -1
					dupli= False
					for i in dup:
						#print("i", i)
						#print("t", t)
						num_t+=1
						if(i== trip_id):
							dupli= True
							num=0
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
								if(num< len(en[num_t].stop_time_update)):
									en[num_t].stop_time_update[num].departure.time= kk.departure.time
									num+=1
							break
					if(dupli== False):
						dup.append(trip_id)
						en.append(t)
						dupli= False
	#print(en)
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
		for i in tt:
			atime=i.departure.time
			stop=i.stop_id
			atimenew=datetime.datetime.fromtimestamp(
				int(atime)
			).strftime('%Y-%m-%d %H:%M:%S')
			if(t.trip.route_id == '1'):
				if(stop[3]== 'S'):
					if(stop=='101S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"101S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='103S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"103S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='112S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"112S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='115S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"115S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='119S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"119S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='120S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"120S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='124S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"124S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='127S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"127S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='137S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"137S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='142S'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"142S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
				elif(stop[3]== 'N'):
					if(stop=='101N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"101N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='103N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"103N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='112N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"112N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='115N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"115N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='119N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"119N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='120N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"120N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='124N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"124N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='127N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"127N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='137N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"137N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='142N'):
						with open("b/1/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"142N.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
			if(t.trip.route_id == '2'):
				if(stop[3]== 'S'):
					if(stop=='201S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"201S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='213S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"213S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='221S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"221S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='224S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"224S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='120S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"120S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='127S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"127S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='132S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"132S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='137S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"137S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='235S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"235S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='239S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"239S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='247S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"247S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
				elif(stop[3]== 'N'):
					if(stop=='201S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"201S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='213S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"213S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='221S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"221S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='224S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"224S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='120S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"120S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='127S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"127S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='132S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"132S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='137S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"137S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='235S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"235S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='239S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"239S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")
					elif(stop=='247S'):
						with open("b/2/"+ str(year)+"_"+ str(month)+"_"+str(day)+"_"+"247S.txt","a") as f:
							f.write(atimenew[11:16]+"   ")