import numpy as np
import pandas as pd
import os
import subprocess
from sklearn.metrics import mutual_info_score

def accuracy_score(y_true, y_pred):

    acc_list = []
    for i in range(y_true.shape[0]):
        set_true = set(np.where(y_true[i])[0])
        set_pred = set(np.where(y_pred[i])[0])

        if len(set_true) == 0 and len(set_pred) == 0:
            tmp_a = 1
        else:
            tmp_a = np.sum(np.where(y_true[i] - y_pred[i] == 0, 1, 0))/y_true.shape[1]

        acc_list.append(tmp_a)

    return np.mean(acc_list)

def hamming_score(y_true, y_pred, normalize=True, sample_weight=None):

    acc_list = []
    for i in range(y_true.shape[0]):
        set_true = set( np.where(y_true[i])[0] )
        set_pred = set( np.where(y_pred[i])[0] )
        #print('\nset_true: {0}'.format(set_true))
        #print('set_pred: {0}'.format(set_pred))
        tmp_a = None
        if len(set_true) == 0 and len(set_pred) == 0:
            tmp_a = 1
        else:
            tmp_a = len(set_true.intersection(set_pred))/\
                    float( len(set_true.union(set_pred)) )
        #print('tmp_a: {0}'.format(tmp_a))
        acc_list.append(tmp_a)
    return np.mean(acc_list)



filePath = "/media/jasminb/ubuntu_data/PerformanceComparison/All_datasets/27Methods/"



print(os.getcwd())
os.chdir(filePath)
print(os.getcwd())
outputPrediction=subprocess.Popen(["find", "-name", "*predValues.csv"], stdout=subprocess.PIPE)
response=outputPrediction.communicate()
#print(response)
outputPrediction  = response[0].decode("utf-8").rsplit("\n")
print(outputPrediction)


from collections import defaultdict
d = defaultdict(dict)



for dataset in outputPrediction:
    pom = dataset.rsplit("/")

    try:
        trueValuesName = dataset.replace("predValues.csv", "trueValues.csv")
        prediction = pd.read_csv(dataset, index_col=[0])
        prediction = prediction.astype("int32").values
        true = pd.read_csv(trueValuesName, index_col=[0])
        true = true.astype("int32").values

        #print(true)
        #print("#############")
        #print(prediction)
        #print(hamming_score(true, prediction))

        res = accuracy_score(true, prediction)


        key = pom[1]
        method = pom[2]

        d[key][method] = res
    except:
        print(dataset)


d["bibtex"]["LP"] =  0.000
d["corel5k"]["LP"] =  0.000
d["delicious"]["LP"] =  0.000
d["delicious"]["MLTSVM"] =  0.000
d["delicious"]["MBR"] = 0.000
d["delicious"]["DEEP4"] = 0.000
d["delicious"]["CLR"] =  0.000
d["stackex_chess"]["TREMLCnew"] = 0.000
d["stackex_cs"]["LP"] =  0.000
d["stackex_philosophy"]["LP"] =  0.000
d["tmc2007_500"]["MLTSVM"] =  0.000



