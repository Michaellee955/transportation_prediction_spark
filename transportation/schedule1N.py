#!/usr/bin/env python

import pandas as pd
import math
import os,sys

line1path='./schedule1N.txt'

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

#104: 42,51,59
def main(column):
    column=column-1
    path=line1path
    df = pd.read_table(path, delim_whitespace=True,names=("South Ferry","Chambers ST","Times Sq 42 ST","59 St Columbus Cir","96 St","137 St City College","168 St","231 St","238 St","Vn Crtlndt Pk 242 St"))
    array=df.values
    c=[]
    for i in range(104):
	    c.append(array[i][column])
    for i in range(44,51):
	    h=int(c[i].split(":")[0])
	    m=c[i].split(":")[1]
	    if h<12:
	        h=str(h+12)
	        c[i]=h+":"+m
    for i in range(52,59):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
    for i in range(60,99):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
        if h==12:
            h=str('00')
            c[i]=h+":"+m
    for i in range(99,104):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h==12:
            h=str('00')
            c[i]=h+":"+m


    seq1=addSeq6(c[41],c[43])
    seq2=addSeq6(c[50],c[52])
    seq3=addSeq5(c[58],c[60])
    cnew=c[:42]+seq1+c[43:51]+seq2+c[52:59]+seq3+c[60:]
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

stop= ["142N", "137N", "127N", "125N", "120N", "115N", "112N", "104N", "103N", "101N"]
for i in range(10):
    test=main(i+1)
    print(test)
    print(len(test))
    with open("a/1/"+stop[i]+".txt","a") as f:
        f.write(str(test)+"\n")






