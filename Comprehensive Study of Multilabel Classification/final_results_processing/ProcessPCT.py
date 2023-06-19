import pandas as pd
import os
import subprocess


path = "/media/jasminb/ubuntu_data/PCTfinished/"


folders = os.listdir(path)

d = {}

for folder in folders:
    print(os.getcwd())

    os.chdir(path + folder +"/")

    output=subprocess.Popen(["find", "./"], stdout=subprocess.PIPE)
    response=output.communicate()

    output  = response[0].decode("utf-8").rsplit("\n")


    meanCsv = []
    for x in output:
        if "_mean.csv" in x:
            meanCsv.append(x)

    dataFramePerDataSet = []
    for x in meanCsv:
        pom = x.rsplit("/")
        df = pd.read_csv(x)

        dataSetName = pom[1]
        methodName = pom[1]

        df["dataSetName"] = folder
        df["method"] = methodName

        dataFramePerDataSet.append(df)

    da = pd.concat(dataFramePerDataSet)
    #da = da.drop(['Unnamed: 0'], axis=1)
    da = da.sort_values(["HAMMING LOSS example based"], axis=0, ascending=True).to_csv(folder+"_PCT_parsedjsons_mean.csv", index=False)
    os.chdir(path)
