from version_control_script import *


dataSetName = sys.argv[1]
methodName = sys.argv[2]

#dataSetName = "ABPM"
#methodName = "BPNN"

try:


    print("Load JSONs")
    jsonFiles = []
    for file in os.listdir(currentDir):
        if ".json" in file:
            jsonFiles.append(file)
            print(file)

    print("Done Parsing Jsons")
    cn = []

    for cnt, file  in enumerate(jsonFiles):
        with open(file, "r") as jfile:
           content = json.load(jfile)

           df = pd.DataFrame(content["measures"], index=[cnt])
           df = df.drop(['Classification report'], axis=1)
           df["name"] = file[:-17]

           cn.append(df)


    frame = pd.concat(cn)
    frame = frame.reset_index()
    frame = frame.drop(["index"], axis=1)
    foldName = [a[-1] for a in list(frame.loc[:, "name"].values)]
    textName = [a[:-1] for a in list(frame.loc[:, "name"].values)]

    for x in range(frame.shape[0]):
        for y in range(frame.shape[1]):
            if 'nan' == frame.iloc[x, y]:
                frame.iloc[x, y] = -1

    frame["fold"] = foldName
    frame["methodConfig"] = textName
    frame = frame.drop(["fold", "name"], axis=1)

    finMean = frame.groupby(by = ["methodConfig"]).mean()

    finMean = finMean.sort_values(by=['HAMMING LOSS example based'], ascending=True)
    finStd = frame.groupby(["methodConfig"]).std()

    finMean = finMean.reset_index()
    finMean.to_csv(dataSetName + "_" +  methodName + "_parsedjsons_mean.csv")


    finStd = finStd.reset_index()
    finStd.to_csv(dataSetName + "_" +  methodName + "_parsedjsons_std.csv")

    import time
    time.sleep(10)  # this is to provide enough time for storage
    print("Done writing file")

except:
    print("CANT WRITE THE FILES")
"""
print(fin.columns)

pomFin = {}
pomFin["ACCURACY example-based"] = fin["ACCURACY example-based"].copy()
pomFin["AUCROC MICRO"] = fin["AUCROC MICRO"].copy()
pomFin["F1 examplbe based"] = fin["F1 examplbe based"].copy()
pomFin["MACRO F1"]  = fin["MACRO F1"].copy()
pomFin["MACRO PRECISION"] = fin["MACRO PRECISION"].copy()
pomFin['MACRO RECALL'] = fin['MACRO RECALL'].copy()
pomFin['MICRO F1'] = fin['MICRO F1'].copy()
pomFin['MICRO PRECISION'] = fin['MICRO PRECISION'].copy()
pomFin['MICRO RECALL']  = fin['MICRO RECALL'].copy()
pomFin['PRECISION example based']  = fin['PRECISION example based'].copy()
pomFin['RECALL example based'] = fin['RECALL example based'].copy()
pomFin['SUBSET ACCURACY'] = fin['SUBSET ACCURACY'].copy()
pomFin[ 'LABEL RANKING AVERAGE PRECISION'] = fin[ 'LABEL RANKING AVERAGE PRECISION']

pomFin["COVARAGE"] = fin["COVARAGE"].copy()
pomFin['HAMMING LOSS exampble based'] = fin['HAMMING LOSS exampble based'].copy()
pomFin['LABEL RANKING LOSS'] = fin['LABEL RANKING LOSS'].copy()
pomFin[ 'ZERO ONE LOSS'] = fin['ZERO ONE LOSS'].copy()

pomFin["methodConfig"] = fin["methodConfig"].copy()


fin = fin.drop(["timeForEval"], axis=1)
#fin = fin.drop(["COVARAGE"], axis=1)

#plt.xticks((np.arange(0, fin.shape[1]), list(fin.columns)))
#plt.yticks(np.arange(0, fin.shape[0]), list(fin.loc[:, "methodConfig"]))


print(np.arange(2, fin.shape[1]).shape)
print(fin.iloc[:, 1:].values.shape)


colors = cm.rainbow(np.linspace(0, 1, len(np.arange(fin.shape[0]))))
print(colors)
for x, c in zip(range(0, fin.shape[0]), colors):


    plt.scatter(0, fin.loc[x, "AUCROC MICRO"], label=fin.iloc[x, 0], c=colors[x])

    plt.scatter(1, fin.loc[x, "ACCURACY example-based"], c=colors[x])
    plt.scatter(2, fin.loc[x, "F1 examplbe based"], c=c)
    plt.scatter(3, fin.loc[x, "PRECISION example based"],  c=colors[x])
    plt.scatter(4, fin.loc[x, "RECALL example based"], c=colors[x])

    plt.scatter(5, fin.loc[x, "MACRO F1"], c=colors[x])
    plt.scatter(6, fin.loc[x, "MACRO PRECISION"],  c=colors[x])
    plt.scatter(7, fin.loc[x, 'MACRO RECALL'], c=colors[x])
    plt.scatter(8, fin.loc[x, "MICRO F1"],  c=colors[x])
    plt.scatter(9, fin.loc[x, "MICRO PRECISION"],  c=colors[x])
    plt.scatter(10, fin.loc[x, "MICRO RECALL"],c=colors[x])

    plt.scatter(11, fin.loc[x, "SUBSET ACCURACY"],  c=colors[x])
    plt.scatter(12, fin.loc[x, "LABEL RANKING AVERAGE PRECISION"], c=colors[x])

    plt.scatter(13,fin.loc[x, "COVARAGE"], c=colors[x])
    plt.scatter(14, fin.loc[x, "HAMMING LOSS exampble based"],  c=colors[x])

    plt.scatter(15, fin.loc[x, "LABEL RANKING LOSS"],  c=colors[x])
    plt.scatter(16, fin.loc[x, "ZERO ONE LOSS"],  c=colors[x])


plt.xticks(np.arange(0, fin.shape[1]), ["AUCROC", "ACCURACY example-based",  "F1 examplbe based", "PRECISION example based", "RECALL example-based", "MACRO F1", "MACRO PRECISION", 'MACRO RECALL',
                                        "MICRO F1", "MICRO PRECISION", "MICRO RECALL", "SUBSET ACCURACY", "LABEL RANKING AVERAGE PRECISION", "COVARAGE",  "HAMMING LOSS exampble based",
                                        "LABEL RANKING LOSS", "ZERO ONE LOSS"], rotation='vertical', fontsize=5)
plt.ylim([0, 1])
plt.legend()
plt.show()
"""