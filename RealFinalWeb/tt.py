import pickle
import os
import numpy as np
from stack import StackingAveragedModels
import pickle
import os

def predict(line,station):
    dir = station[-1]
    station = station[:-1]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    name = line+'_'+station+'_'+dir
    model_dir = dir_path+'/models/{}.csv.sav'.format(name)
    # load the model from disk
    loaded_model = pickle.load(open(model_dir, 'rb'))

    dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cur_dir = dir + '/streaming/test.json'

    with open(cur_dir,'rb') as file:
        weather_dict = pickle.load(file)
    test = [weather_dict['hour'],weather_dict['temp'],weather_dict['pressure'],
            weather_dict['humidity'],weather_dict['wind_sp'],
            weather_dict['clouds'],weather_dict['weather_code'],30]
    test = np.array(test).reshape(1,-1)
    y_test_pred = loaded_model.predict(test)
    return y_test_pred
