import sys
import numpy as np
import datetime
import os
import time
import csv
'''
while(1):
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	time.sleep(5)'''

time_now= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("year", time_now[:4])
print("month", time_now[5:7])
print("day", time_now[8:10])
print("hour", time_now[11:13])
print("minute", time_now[14:16])
print("second", time_now[17:19])


filename = 'real_time_'+time_now[11:13]+'.csv'

with open(filename, 'a') as file:
    writer = csv.writer(file)
    writer.writerow(time_now[:4])