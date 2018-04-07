import os
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json


sc = SparkContext(master='local[2]')
filename = "real_time.csv"
dataFile = sc.textFile(filename)

print(dataFile.top(1))

