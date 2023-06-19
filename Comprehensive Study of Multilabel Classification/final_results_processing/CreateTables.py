import pandas as pd
import os
import subprocess


#resultsPath = "/media/jasminb/ubuntu_data/PerformanceComparison/All_datasets/neData/"
#resultsPath = "/media/jasminb/ubuntu_data/PerformanceComparison/All_datasets/zaPaper/AllMethods/"
resultsPath = "/media/jasminb/ubuntu_data/PerformanceComparison/All_datasets/zaPaper/DBNcomparison/"

#print(os.getcwd())
os.chdir(resultsPath)
#print(os.getcwd())
output=subprocess.Popen(["find", "./"], stdout=subprocess.PIPE)
response=output.communicate()
#print(response)
output  = response[0].decode("utf-8").rsplit("\n")


meanCsv = []
for x in output:
    if "_mean.csv" in x:
        meanCsv.append(x)

numberMethods = 4
dataFramePerDataSet = []

for x in meanCsv:
    print(x)
    pom = x.rsplit("/")

    df = pd.read_csv(x)

    if "_PCT_" in x:
        #print(x)
        df = df.T
        clName = ["Unnamed: 0"]
        df.columns = df.iloc[0, :]
        for m in list(df.columns):
            clName.append(m)
        print(df.shape)
        df = pd.DataFrame(df.iloc[1, :].values.reshape((32, 1)))
        df = df.T
        df = df.reset_index()
        df.columns = clName


    print(df.shape)
    #print(pom)
    dataSetName = pom[1]
    methodName = pom[2]

    df["dataSetName"] = dataSetName
    df["method"] = methodName

    dataFramePerDataSet.append(df)


# ALWAYS CHECK THIS SCRIPT
finSet = pd.concat(dataFramePerDataSet)
finSet = finSet.reset_index()
finSet = finSet.iloc[:, 2:]

groups = finSet.loc[:, ["dataSetName", "method"]].groupby(["dataSetName"]).groups
indeciesGroups = groups.keys()

dic = {}


measures = ['ACCURACY example-based', 'AUCROC MACRO', 'AUCROC MICRO',
       'AUCROC SAMPLES', 'AUCROC WEIGHTED', 'AUPRC MACRO', 'AUPRC MICRO',
       'AUPRC SAMPLE', 'AUPRC WEIGHTED', 'COVARAGE', 'F1 example based',
       'HAMMING LOSS example based', 'LABEL RANKING AVERAGE PRECISION',
       'LABEL RANKING LOSS', 'MACRO F1', 'MACRO PRECISION', 'MACRO RECALL',
       'MICRO F1', 'MICRO PRECISION', 'MICRO RECALL', 'ONE ERROR',
       'PRECISION example based', 'RECALL example based', 'SUBSET ACCURACY',
       'WEIGHTED F1', 'WEIGHTED PRECISION', 'WEIGHTED RECALL',
       'ZERO ONE LOSS', 'testTime',
       'timeForEval', 'trainTime']





for cnt, measure in enumerate(measures):
    d = {}
    for key in list(indeciesGroups):

        q = finSet.loc[:, measures].loc[groups[key], measure]
        q = q.reset_index()

        d[key] = q.iloc[:, 1].values
        print("Dataset {} has {} number of columns".format(key, len(list(d[key]))))

    nn = pd.DataFrame(d).T
    nn.columns = finSet.loc[:, "method"].values[:numberMethods]
    print(len(list(nn.columns)))
    dic[finSet.loc[:, measures].columns[cnt]] = nn


for x in list(dic.keys()):
    dic[x].astype("float32").round(decimals=3).to_csv(x.rsplit("/",)[0].replace(" ", "_").replace("-", "_")  + ".csv")
