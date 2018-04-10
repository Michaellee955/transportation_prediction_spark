#!/usr/bin/env python

import pandas as pd
import math
import os,sys

stop=int(sys.argv[1])
line1path='./schedule2S.txt'
log=str(sys.argv[2])

def addSeq8(start,end):
    hour1=start.split(":")[0]
    minute1=start.split(":")[1]
    hour2=end.split(":")[0]
    minute2=end.split(":")[1]
    startm=int(hour1)*60+int(minute1)
    endm=int(hour2)*60+int(minute2)
    interval=endm-startm
    step=interval/8
    step=math.floor(step)
    if interval%8==0:
        step=step-1
    curr=startm
    seq=[]
    for i in range(step):
        curr=curr+8
        h=math.floor(curr/60)
        m=curr%60
        store=str(h)+":"+str(m)
        seq.append(store)
    return seq

def addSeq7(start,end):
    hour1=start.split(":")[0]
    minute1=start.split(":")[1]
    hour2=end.split(":")[0]
    minute2=end.split(":")[1]
    startm=int(hour1)*60+int(minute1)
    endm=int(hour2)*60+int(minute2)
    interval=endm-startm
    step=interval/7
    step=math.floor(step)
    if interval%7==0:
        step=step-1
    curr=startm
    seq=[]
    for i in range(step):
        curr=curr+7
        h=math.floor(curr/60)
        m=curr%60
        store=str(h)+":"+str(m)
        seq.append(store)
    return seq

def addSeq9(start,end):
    hour1=start.split(":")[0]
    minute1=start.split(":")[1]
    hour2=end.split(":")[0]
    minute2=end.split(":")[1]
    startm=int(hour1)*60+int(minute1)
    endm=int(hour2)*60+int(minute2)
    interval=endm-startm
    step=interval/9
    step=math.floor(step)
    if interval%9==0:
        step=step-1
    curr=startm
    seq=[]
    for i in range(step):
        curr=curr+9
        h=math.floor(curr/60)
        m=curr%60
        store=str(h)+":"+str(m)
        seq.append(store)
    return seq
flag1=True

#95: 63,70,78
def main(column):
    global flag1
    column=column-1
    path=line1path
    df = pd.read_table(path, delim_whitespace=True,names=("Wakefield 241 St","E 180 St","149 St","135 St","96 St","Times Sq 42 St","14 St","Chambrs St","Atlantic Av-Barclays Ctr","Franklin Av","Flatbush"))
    array=df.values
    c=[]
    for i in range(95):
        c.append(array[i][column])
    for i in range(63):
        if c[i]!='—':
            h=int(c[i].split(":")[0])
            m=c[i].split(":")[1][:2]
            if h==12:
                h=str('00')
            c[i]=str(h)+":"+m
    for i in range(64,70):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
    for i in range(71,78):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
    for i in range(79,95):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h==12:
            h=str('00')
            flag1=False
            c[i]=h+":"+m   
        elif h<12 and flag1==True:
            h=str(h+12)
            c[i]=h+":"+m  

#95: 63,70,78
    seq1=addSeq8(c[62],c[64])
    seq2=addSeq7(c[69],c[71])
    seq3=addSeq9(c[77],c[79])
    cnew=c[:63]+seq1+c[64:70]+seq2+c[71:78]+seq3+c[79:]
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

stop= ["201S", "213S", "221S", "224S", "120S", "127S", "132S", "137S", "235S", "239S", "247S"]
for i in range(11):
    flag1=True
    test=main(i+1)
    print(test)
    print(len(test))
    with open("a/"+stop[i]+".txt","a") as f:
        f.write(str(test)+"\n")




