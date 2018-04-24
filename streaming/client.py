from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import pickle
import json

def printrdd(x):
    global counts,dict,temp,pressure,humidity,wind_sp,wind_de,clouds,weather_code
    ts,mo,da,ho,mi,te,pr,hu,ws,wd,cl,wc=x.split(',')

    if mi=='0':
        init_dict()

    dict['temp'] += float(te)/counts
    dict['pressure'] += float(pr)/counts
    dict['humidity'] += float(hu)/counts
    dict['wind_sp'] += float(ws)/counts
    dict['wind_de'] += float(wd)/counts
    dict['clouds'] += float(cl)/counts
    dict['weather_code'] += float(wc)/counts
    filename = 'test'
    with open(filename,'wb') as myfile:
        pickle.dump(dict,myfile)

def init_dict():
    global dict

    dict['temp'] = 0
    dict['pressure'] = 0
    dict['humidity'] = 0
    dict['wind_de'] = 0
    dict['wind_sp'] = 0
    dict['clouds'] = 0
    dict['weather_code'] = 0

if __name__ == '__main__':
    global dict,temp,pressure,humidity,wind_sp,wind_de,clouds,weather_code
    dict = {}
    init_dict()
    sc = SparkContext('local[2]','weather')
    ssc = StreamingContext(sc,10)
    hd = 'hdfs://localhost:9000/User'
    local = '/Users/michael/OneDrive/Documents/large_data_streaming/project/streaming/bb'
    lines = ssc.textFileStream(local)
    global counts
    counts = lines.count()
    lines.foreachRDD(lambda rdd: rdd.foreach(printrdd))
    ssc.start()
    ssc.awaitTermination()