#!/usr/bin/env python

import pandas as pd
import math
import os,sys

line1path='./schedule2N.txt'

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
flag1=True
flag2=True

#95:19,28,55
def main(column):
    global flag1,flag2,flag3
    column=column-1
    path=line1path
    df = pd.read_table(path, delim_whitespace=True,names=("Flatbush","Franklin Av","Atlantic Av-Barclays Ctr","Chambrs St","14 St","Times Sq 42 St","96 St","135 St","149 St","E 180 St","Wakefield 241 St"))
    array=df.values
    c=[]
    for i in range(95):
        c.append(array[i][column])
    for i in range(19):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h==12:
            h=str('00')
            c[i]=h+":"+m
    for i in range(20,28):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h==12:
            flag1=False
        if h<12 and flag1==False:
            h=str(h+12)
            c[i]=h+":"+m
    for i in range(29,55):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1][:2]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
    for i in range(56,95):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h==12:
            h=str('00')
            flag2=False
            c[i]=h+":"+m
        elif h<12 and flag2==True:
            h=str(h+12)
            c[i]=h+":"+m

    '''for i in range(22,28):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
    for i in range(29,55):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1][:2]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
    for i in range(56,85):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h<12:
            h=str(h+12)
            c[i]=h+":"+m
        if h==12:
            h=str('00')
            c[i]=h+":"+m
    for i in range(85,95):
        h=int(c[i].split(":")[0])
        m=c[i].split(":")[1]
        if h==12:
            h=str('00')
            c[i]=h+":"+m  '''

#95:19,28,55
    seq1=addSeq9(c[18],c[20])
    seq2=addSeq8(c[27],c[29])
    seq3=addSeq7(c[54],c[56])
    cnew=c[:19]+seq1+c[20:28]+seq2+c[29:55]+seq3+c[56:]
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

stop= ["247N","239N","235N","137N","132N","127N","120N","224N","221N","213N","201N"]
for i in range(11):
    flag1=True
    flag2=True
    test=main(i+1)
    print(test)
    print(len(test))
    with open("a/"+stop[i]+".txt","a") as f:
        f.write(str(test)+"\n")



