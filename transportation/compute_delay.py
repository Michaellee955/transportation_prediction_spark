import sys
import numpy as np
import datetime


stop= ["101S", "103S", "112S", "115S", "119S", "120S", "124S", "127S", "137S", "142S"]

for day in range(1, 15):
	if(datetime.date(2017, 9, day).weekday()>4):
		continue
	for stop_i in range(10):
		schedule= []
		s= stop[stop_i]
		s_str=[]
		a= open("a/"+ s+ ".txt").read()
		for i in range(len(a)):
			if(a[i: i+2]== "['" or a[i: i+2]== " '"):
				temp= int(a[i+2:i+4])*60+int(a[i+5:i+7])
				s_str.append(a[i+2:i+7])
				schedule.append(temp)

		real_time= []
		b= open("b/1/2017_9_"+str(day)+"_"+s+".txt").read()
		for i in range(0, len(b),8):
			temp= int(b[i:i+2])*60+int(b[i+3:i+5])
			real_time.append(temp)
		real_time= np.sort(real_time)

		num=0
		delay=[]
		for i in range(len(real_time)):
			while((num+1)< len(schedule) and schedule[num+1]<= real_time[i]):
				num+=1
			string= str(s_str[num]+": "+str(real_time[i]- schedule[num])+"\n")
			with open("delay/"+"2017_9_"+str(day)+"_"+s+".txt","a") as f:
				f.write(string)

