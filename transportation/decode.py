from google.transit import gtfs_realtime_pb2
from astropy.table import Table, Column
import numpy as np
import requests
import datetime
#path2='https://datamine-history.s3.amazonaws.com/gtfs-2014-09-17-09-36'
#path2='https://datamine-history.s3.amazonaws.com/gtfs-2014-09-17-09-36'

route_input='1'
stop_input='103S'
array=[]
aa= False
feed = gtfs_realtime_pb2.FeedMessage()
dup = []
dupli = False
en=[]
path='https://datamine-history.s3.amazonaws.com/gtfs'
year= 2017
month= 9
day= 17
hour= -1
duplicate= -2
day_in_month=(31,28,31,30,31,30,31,31,30,31,30,31)
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
		response = requests.get(tem)
		feed.ParseFromString(response.content)
		all_num=0
		for entity in feed.entity:		
		  	if entity.HasField('trip_update'):
			    t=entity.trip_update
			    tri= t.trip
			    trip_id= tri.trip_id
			    num_t= -1
			    dupli= False
			    for i in dup:
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
			    			num+=1
			    		for kk in tt:
			    			en[num_t].stop_time_update[num].departure.time= kk.departure.time
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
	if(year_num!= int(year)):
		if(month_num!= 12 and day_num!=31):
			continue
	if(month_num!= int(month)):
		if(day_num!= day_in_month[month_num-1]):
			continue
	if(day_num!= int(day)):
		if(hour_num!=23):
			continue
	for i in tt:
	    atime=i.arrival.time
	    stop=i.stop_id
	    atimenew=datetime.datetime.fromtimestamp(
	    	int(atime)
		).strftime('%Y-%m-%d %H:%M:%S')
	    if t.trip.route_id ==route_input and stop==stop_input:
	    	#print("trip_id", tri.trip_id)
	    	array.append(atimenew[11:16])
	    	#print("time", atimenew[11:16])
	    	#print(tri.trip_id)




		    #print("whole:",entity)
		    #print("******************")num1=0
#print(table)
#with open(log,"a") as f: 
	#f.write(str(tf)+' '+str(tf-ts)+' '+str(tn/1000)+' '+str(tc/1000)+' '+realBitrate+' '+serverIP+' '+name+"\n")
	#f.write(str(table))	
print(array)
print(len(array))