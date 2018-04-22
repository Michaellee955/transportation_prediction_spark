from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext('local[2]','weather')
ssc = StreamingContext(sc,10)
lines = ssc.textFileStream('/Users/michael/OneDrive/Documents/large_data_streaming/project/streaming/test')

counts = lines.flatMap(lambda line: line.split(",")) \
    .map(lambda word:(word, 1)) \
    .reduceByKey(lambda a,b:a+b)

counts.pprint()

ssc.start()
ssc.awaitTermination()