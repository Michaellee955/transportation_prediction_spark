import sys
import numpy as np
import datetime
import os

stops= ["101S", "103S", "112S", "115S", "119S", "120S", "124S", "127S", "137S", "142S", "142N", "137N", "127N", "125N", "120N", "115N", "112N", "104N", "103N", "101N", 
"201S", "213S", "221S", "224S", "120S", "127S", "132S", "137S", "235S", "239S", "247S", "247N","239N","235N","137N","132N","127N","120N","224N","221N","213N","201N"]
day_in_month=(31,28,22,30,31,30,31,31,30,31,30,31)
for month in range(1, 3):
	for day in range(1, day_in_month[month-1]+1):
		if(datetime.date(2018, month, day).weekday()>4):
			continue
		for stop_i in range(len(stops)):
			schedule= []
			s= stops[stop_i]
			s_str=[]
			if(stop_i< 20):
				a= open("a/1/"+ s+ ".txt").read()
			else:
				a= open("a/2/"+ s+ ".txt").read()
			for i in range(len(a)):
				if(a[i: i+2]== "['" or a[i: i+2]== " '"):
					temp= int(a[i+2:i+4])*60+int(a[i+5:i+7])
					s_str.append(a[i+2:i+7])
					schedule.append(temp)

			real_time= []
			if(stop_i< 20 and os.path.isfile("b/1/2018_"+str(month)+"_"+str(day)+"_"+s+".txt")== False):
				continue
			elif(stop_i>= 20 and os.path.isfile("b/2/2018_"+str(month)+"_"+str(day)+"_"+s+".txt")== False):
				continue
			else:
				if(stop_i< 20):
					b= open("b/1/2018_"+str(month)+"_"+str(day)+"_"+s+".txt").read()
				else:
					b= open("b/2/2018_"+str(month)+"_"+str(day)+"_"+s+".txt").read()
			for i in range(0, len(b),8):
				temp= int(b[i:i+2])*60+int(b[i+3:i+5])
				real_time.append(temp)
			real_time= np.sort(real_time)

			num=0
			delay=[]
			for i in range(len(real_time)):
				while((num+1)< len(schedule) and schedule[num+1]<= real_time[i]):
					num+=1
				if((num+1)>= len(schedule) or (real_time[i]- schedule[num])<(schedule[num+1]- real_time[i])):
					string= str(s_str[num]+": "+str(real_time[i]- schedule[num])+"\n")
				else:
					string= str(s_str[num]+": "+str(-1*(schedule[num+1]- real_time[i]))+"\n")
				if(stop_i< 20):
					with open("delay/1/2018_"+str(month)+"_"+str(day)+"_"+s+".txt","a") as f:
						f.write(string)
				else:
					with open("delay/2/2018_"+str(month)+"_"+str(day)+"_"+s+".txt","a") as f:
						f.write(string)					

