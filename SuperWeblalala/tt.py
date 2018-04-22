import pickle
import os
import numpy as np
from stack import StackingAveragedModels

def predict(line,station,dir):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    name = line+'_'+station+'_'+dir
    model_dir = dir_path+'/models/{}.csv.sav'.format(name)
    # load the model from disk
    loaded_model = pickle.load(open(model_dir, 'rb'))



    test = [0,297.61,1018,54,5,90,4,31]
    test = np.array(test).reshape(1,-1)
    #y_train_pred = loaded_model.predict(test)
    y_test_pred = loaded_model.predict(test)

    return y_test_pred
