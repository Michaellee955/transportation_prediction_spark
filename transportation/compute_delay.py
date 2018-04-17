import sys
import numpy as np
import datetime
import os

stop_1= ["142N", "137N", "127N", "125N", "120N", "115N", "112N", "104N", "103N", "101N"]
stop_2= ["201N", "213N", "221N", "224N", "120N", "127N", "132N", "137N", "235N", "239N", "247N"]

for day in range(1, 15):
	if(datetime.date(2017, 9, day).weekday()>4):
		continue
	for stop_i in range(len(stop_2)):
		schedule= []
		s= stop_2[stop_i]
		s_str=[]
		a= open("a/2/"+ s+ ".txt").read()
		for i in range(len(a)):
			if(a[i: i+2]== "['" or a[i: i+2]== " '"):
				temp= int(a[i+2:i+4])*60+int(a[i+5:i+7])
				s_str.append(a[i+2:i+7])
				schedule.append(temp)

		real_time= []
		if(os.path.isfile("b/2/2017_9_"+str(day)+"_"+s+".txt")== False):
			continue
		else:
			b= open("b/2/2017_9_"+str(day)+"_"+s+".txt").read()
		for i in range(0, len(b),8):
			temp= int(b[i:i+2])*60+int(b[i+3:i+5])
			real_time.append(temp)
		real_time= np.sort(real_time)

		num=0
		delay=[]
		for i in range(len(real_time)):
			while((num+1)< len(schedule) and schedule[num+1]<= real_time[i]):
				num+=1
			if((real_time[i]- schedule[num])<(schedule[num+1]- real_time[i])):
				string= str(s_str[num]+": "+str(real_time[i]- schedule[num])+"\n")
			else:
				string= str(s_str[num]+": "+str(-1*(schedule[num+1]- real_time[i]))+"\n")
			with open("delay/2/"+"2017_9_"+str(day)+"_"+s+".txt","a") as f:
				f.write(string)

