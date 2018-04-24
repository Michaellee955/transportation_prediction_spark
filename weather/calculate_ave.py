import csv
import numpy as np
import key
import time
import shutil
import os

def cal_ave(path):
	data= []
	with open(path,"r") as f:
		reader= csv.reader(f)
		num=0
		for row in (reader):
			if(num==0):
				num=1
				continue
			row = row[6:]
			row = [float(i) for i in row]
			data.append(row)
	data= np.array(data[1:])
	data= np.reshape(data, (-1, 6))

	ave= np.sum(data, axis= 0)
	return ave