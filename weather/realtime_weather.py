import csv
import requests
import time
import datetime
import key
"04259690c79731a13bcf68ea887225bb"
city_id = 5128581
APP_ID = key.APPID
url = "http://api.openweathermap.org/data/2.5/weather?id={}&APPID={}".format(city_id,APP_ID)

def getweather(weather):
    num_max = 0
    for i in range(len(weather)):
        num = int(weather[i]['id']/10)
        if num>num_max:
            num_max = num
    return num_max

def gettime():
    pre = datetime.datetime.now()
    year = pre.year
    month = pre.month
    date = pre.day
    hour = pre.hour
    minute = pre.minute
    year = "{0:0=4d}".format(year)
    month_stamp = "{0:0=2d}".format(month)
    date_stamp = "{0:0=2d}".format(date)
    hour_stamp = "{0:0=2d}".format(hour)
    minute_stamp = "{0:0=2d}".format(minute)
    timestamp = int(year+month_stamp+date_stamp+hour_stamp+minute_stamp)

    return timestamp,month,date,hour,minute

filename = 'real_time.csv'

with open(filename, 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    head = ["timestamp","month","date","hour","minute","temp","pressure","humidity","wind speed","wind direction","clouds","weather code"]
    wr.writerow(head)

while(True):
    try:
        timestamp, month, date, hour, minute = gettime()
        real_weather = requests.get(url)
        weather = real_weather.json()
        temp = weather['main']['temp']
        pressure = weather['main']['pressure']
        humidity = weather['main']['humidity']
        wind_sp = weather['wind']['speed']
        wind_de = weather['wind']['deg']
        cloud = weather['clouds']['all']
        weather_code = getweather(weather['weather'])
        new_row = [timestamp,month,date,hour,minute,temp,pressure,humidity,wind_sp,wind_de,cloud,weather_code]

        with open(filename,'a') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        print("one more piece of weather imported")
        time.sleep(60)
    except:
        print("data format not matched or key rejected, waiting for 10 min")
        time.sleep(600)
