import json
from pprint import pprint
import csv

def gettime(timeline):
    hour_ori = timeline.split(" ")[1]
    hour = hour_ori.split(":")[0]
    date_ori = timeline.split(" ")[0]
    month = date_ori.split("-")[1]
    date = date_ori.split("-")[2]
    return month,date,hour

def getweather(weather):
    num_max = 0
    for i in range(len(weather)):
        num = 10 * (ord(weather[i]["icon"][0]) - 48) + (ord(weather[i]["icon"][1]) - 48)
        if num>num_max:
            num_max = num
    return num_max

filename = "newyork5.json"
data = json.load(open(filename))
temp = []
pressure = []
humidity = []
months = []
dates = []
hours = []
wind_sp = []
wind_de = []
clouds = []
icons = []
for i in range(len(data)):
    temp.append(data[i]['main']['temp'])
    pressure.append(data[i]['main']['pressure'])
    humidity.append(data[i]['main']['humidity'])
    month,date,hour = gettime(data[i]["dt_iso"])
    months.append(month)
    dates.append(date)
    hours.append(hour)
    wind_sp.append(data[i]["wind"]["speed"])
    wind_de.append(data[i]["wind"]["deg"])
    clouds.append(data[i]["clouds"]["all"])
    icons.append(getweather(data[i]["weather"]))

with open('weather.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    head = ["month","date","hour","temp","pressure","humidity","wind speed","wind direction","clouds","weather code"]
    wr.writerow(head)
    for i in range(len(data)):
        weather = [months[i],dates[i],hours[i],temp[i],pressure[i],humidity[i],wind_sp[i],wind_de[i],clouds[i],icons[i]]
        print(weather)
        wr.writerow(weather)
