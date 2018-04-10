#!/usr/bin/env python

import pandas as pd
import math
import os,sys

line1path='./schedule1S.txt'

def addSeq5(start,end):
    hour1=start.split(":")[0]
    minute1=start.split(":")[1]
    hour2=end.split(":")[0]
    minute2=end.split(":")[1]
    startm=int(hour1)*60+int(minute1)
    endm=int(hour2)*60+int(minute2)
    interval=endm-startm
    step=interval/5
    step=math.floor(step)
    if interval%5==0:
        step=step-1
    curr=startm
    seq=[]
    for i in range(step):
        curr=curr+5
        h=math.floor(curr/60)
        m=curr%60
        store=str(h)+":"+str(m)
        seq.append(store)
    return seq

def addSeq6(start,end):
    hour1=start.split(":")[0]
    minute1=start.split(":")[1]
    hour2=end.split(":")[0]
    minute2=end.split(":")[1]
    startm=int(hour1)*60+int(minute1)
    endm=int(hour2)*60+int(minute2)
    interval=endm-startm
    step=interval/6
    step=math.floor(step)
    if interval%6==0:
        step=step-1
    curr=startm
    seq=[]
    for i in range(step):
        curr=curr+6
        h=math.floor(curr/60)
        m=curr%60
        store=str(h)+":"+str(m)
        seq.append(store)
    return seq
#105: 68,73,79
def main(column):
    column=column-1
    path=line1path
    df = pd.read_table(path, delim_whitespace=True,names=("Vn Crtlndt Pk 242 ST","238 ST","168 ST","137 ST City College","103 ST","96 ST","66 ST Lincoln Ctr","Times Sq 42 ST","Chambers ST","South Ferry"))
    array=df.values
    c=[]
    for i in range(105):
	    c.append(array[i][column])
    for i in range(68):
        if c[i]!='—':
            h=int(c[i].split(":")[0])
            m=c[i].split(":")[1]
            if h==12:
    	        h=str('00')
    	        c[i]=h+":"+m
    for i in range(74,79):
	    h=int(c[i].split(":")[0])
	    m=c[i].split(":")[1]
	    if h<12:
	        h=str(h+12)
	        c[i]=h+":"+m
    for i in range(80,105):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
        if h==12:
            h=str('00')
            c[i]=h+":"+m

    seq1=addSeq5(c[67],c[69])
    seq2=addSeq6(c[72],c[74])
    seq3=addSeq5(c[78],c[80])
    cnew=c[:68]+seq1+c[69:73]+seq2+c[74:79]+seq3+c[80:]
    for i in cnew:
        if i=='—':
            cnew.remove(i)
    for i in range(len(cnew)):
        h=int(cnew[i].split(":")[0])
        m=int(cnew[i].split(":")[1])
        if h<10:
            h='0'+str(h)
        if m<10:
            m='0'+str(m)
        h=str(h)
        m=str(m)
        cnew[i]=h+":"+m
    return cnew

stop= ["101S", "103S", "112S", "115S", "119S", "120S", "124S", "127S", "137S", "142S"]
for i in range(10):
    test=main(i+1)
    print(test)
    print(len(test))
    with open("a/"+stop[i]+".txt","a") as f:
        f.write(str(test)+"\n")





