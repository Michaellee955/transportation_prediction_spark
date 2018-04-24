from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import pickle

def averdd(x):
    global dict,counts,i
    i += 1
    print(i)
    ts, mo, da, ho, mi, te, pr, hu, ws, wd, cl, wc = x.split(',')
    if mi=='0':
        init_dict()
    dict['hour'] = ho
    dict['temp'] += float(te)/counts
    dict['pressure'] += float(pr)/counts
    dict['humidity'] += float(hu)/counts
    dict['wind_sp'] += float(ws)/counts
    dict['wind_de'] += float(wd)/counts
    dict['clouds'] += float(cl)/counts
    dict['weather_code'] += float(wc)/counts
    filename = 'test.json'
    with open(filename,'wb') as file:
        pickle.dump(dict,file)

def init_dict():
    global dict

    dict['hour'] = 0
    dict['temp'] = 0
    dict['pressure'] = 0
    dict['humidity'] = 0
    dict['wind_de'] = 0
    dict['wind_sp'] = 0
    dict['clouds'] = 0
    dict['weather_code'] = 0

def f(x):
    global counts
    counts = x.take(1)
    for item in counts:
        counts = item

if __name__ == '__main__':
    i = 0
    dict = {}
    init_dict()
    sc = SparkContext('local[2]','weather')
    ssc = StreamingContext(sc,10)
    #/large_data_streaming/project/streaming/bb
    local = '/Users/michael/OneDrive/Documents/large_data_streaming/project/streaming/datasets_streaming'
    lines = ssc.textFileStream(local)
    count = lines.count()
    count.foreachRDD(f)
    lines.foreachRDD(lambda rdd: rdd.foreach(averdd))
    ssc.start()
    ssc.awaitTermination()