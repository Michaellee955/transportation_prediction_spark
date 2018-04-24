import json
import csv
import os
import pickle

def convert(filename):
    dict = {}
    with open(filename,'r') as file:
        reader = csv.reader(file)
        next(reader,None)
        for row in reader:
            timestamp = row[0]+row[1]+row[2]+row[3] # YYYYMMDDHH
            content = row[1]+' '+row[2]+' '+row[3]+' '+row[4]+' '+row[5]+' '+row[6]+' '+row[7]+' '+row[8]+' '+row[9]+' '+row[10]
            dict[timestamp] = content
        return dict

def gettime(timeline):
    hour_ori = timeline.split(" ")[1]
    hour = hour_ori.split(":")[0]
    date_ori = timeline.split(" ")[0]
    year = date_ori.split("-")[0]
    month = date_ori.split("-")[1]
    date = date_ori.split("-")[2]
    return year,month,date,hour

def getweather(weather):
    num_max = 0
    for i in range(len(weather)):
        num = 10 * (ord(weather[i]["icon"][0]) - 48) + (ord(weather[i]["icon"][1]) - 48)
        if num>num_max:
            num_max = num
    return num_max

def parse_weather(filename):
    data = json.load(open(filename))
    temp = []
    pressure = []
    humidity = []
    years = []
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
        year,month,date,hour = gettime(data[i]["dt_iso"])
        years.append(year)
        months.append(month)
        dates.append(date)
        hours.append(hour)
        wind_sp.append(data[i]["wind"]["speed"])
        wind_de.append(data[i]["wind"]["deg"])
        clouds.append(data[i]["clouds"]["all"])
        icons.append(getweather(data[i]["weather"]))

    with open('weather.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        head = ["year","month","date","hour","temp","pressure","humidity","wind speed","wind direction","clouds","weather code"]
        wr.writerow(head)
        for i in range(len(data)):
            weather = [years[i],months[i],dates[i],hours[i],temp[i],pressure[i],humidity[i],wind_sp[i],wind_de[i],clouds[i],icons[i]]
            print(weather)
            wr.writerow(weather)

def combine(filename_weather, filename_trans,LINE):
    with open(filename_weather, "rb") as myFile:
        weather_dict = pickle.load(myFile)
        print(weather_dict)

    with open(filename_trans,'r') as myfile:
        reader = csv.reader(myfile)
        result = []
        for row in reader:
            timestamp = row[0]
            try:
                weather = weather_dict[timestamp]
                cur = list(weather.split(" "))
                for i in range(1,6):
                    cur.append(row[i])
                result.append(cur)
            except KeyError:
                pass
        save(result,LINE)

def save(result,LINE):
    feature_space = 'feature_space_{}.csv'.format(LINE)
    with open(feature_space, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for item in result:
            wr.writerow(item)

class parse_delay_files(object):
    def __init__(self,LINE):
        self.LINE = LINE
        self.dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.feature_space = 'filename_trans_{}.csv'.format(self.LINE)

    def title_process(self,title):
        title_main = title.replace('.txt','')
        year,month,date,station = title_main.split('_')
        month = "{0:0=2d}".format(int(month))
        date = "{0:0=2d}".format(int(date))
        print(month)
        return year,str(month),str(date),station,self.LINE

    def save(self,line):
        with open(self.feature_space,'a') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            for item in line:
                wr.writerow(item)

    def minute_window(self,title,reader):
        year,month,date,station,line_num = self.title_process(title)
        station_id = station[:-1]
        station_dir = station[-1:]
        #dict_ave = {}
        #dict_count = {}
        cur_line = []
        for line in reader:
            content = line[0]
            hour = int(content.split(':')[0])
            minute = int(content.split(':')[1])
            delay = int(content.split(':')[2])
            if delay > 2:
                delay=2
            elif delay<-2:
                delay = -2
            """
            if delay >-10  and delay <10:
                if None is dict_ave.get(hour):
                    dict_ave[hour] = min(10,delay)
                else:
                    dict_ave[hour] += delay
                if None is dict_count.get(hour):
                    dict_count[hour] = 1
                else:
                    dict_count[hour] += 1
        cur_line = []
        for i,key in enumerate(dict_ave):
            dict_ave[key] = dict_ave[key]/dict_count[key]
            hour = "{0:0=2d}".format(key)
            minute = "{0:0=2d}".format(minute)
            timestamp = str(year)+str(month)+str(date)+str(hour)
            print(timestamp)
            cur_line.append([timestamp,line_num,station_id,station_dir,dict_ave[key]])
        """
            hour = "{0:0=2d}".format(hour)
            minute = "{0:0=2d}".format(minute)
            timestamp = str(year) + str(month) + str(date) + str(hour)
            cur_line.append([timestamp,minute,line_num,station_id,station_dir,delay])
        self.save(cur_line)



    def file_iterate(self):
        dir = self.dir_path+'/transportation/delay/{}'.format(self.LINE)
        for file in os.listdir(dir):
            filename = os.fsdecode(file)
            if filename != '.DS_Store':
                cur_file = dir + '/' + filename
                with open(cur_file,'r') as delay_file:
                    reader = csv.reader(delay_file)
                    self.minute_window(filename,reader)

class construct_dataset(object):

    def __init__(self,filename):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.objpath = self.dir_path + '/datasets'
        self.file = filename

    def gene_dict(self):
        with open(self.file,'r')as origin_file:
            reader = csv.reader(origin_file)
            dict_dataset = {}
            for line in reader:
                index = line[-4]+'_'+line[-3]+'_'+line[-2]
                features = []
                for i in range(len(line)):
                    if i != 11 and i!=12 and i!=13:
                        features.append(line[i])
                if None is dict_dataset.get(index):
                    dict_dataset[index] = []
                    dict_dataset[index].append(features)
                else:
                    dict_dataset[index].append(features)
        return dict_dataset
    def save_dataset(self):
        dict = self.gene_dict()
        for item, key in enumerate(dict):
            objfile_name = self.objpath+'/'+key+'.csv'
            print(objfile_name)
            with open(objfile_name,'w') as dataset_file:
                wr = csv.writer(dataset_file, quoting=csv.QUOTE_ALL)
                for line in dict[key]:
                    wr.writerow(line)




if __name__ == '__main__':

    #filename_meta = "newyork5.json"
    #parse_weather(filename_meta)
    filename_result = 'weather.csv'
    filename_dict = 'weatherDict.txt'
    filename_trans = 'filename_trans_2.csv'
    filename_feature_1 = 'feature_space_1.csv'
    filename_feature_2 = 'feature_space_2.csv'
    dict = convert(filename_result)

    # save a dictionary containing weather data
    #with open(filename_dict, "wb") as myFile:
    #    pickle.dump(dict, myFile)

    # parse the delayed time files
    #parser = parse_delay_files(2)
    #parser.file_iterate()
    #combine(filename_dict,filename_trans,2)

    #construct dataset
    constructor = construct_dataset(filename_feature_2)
    constructor.save_dataset()
