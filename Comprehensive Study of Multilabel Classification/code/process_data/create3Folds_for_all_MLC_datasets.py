from version_control_script import *
from algorithmConfiguration import *
from dataSetsPreprocessing import *

import random
dataSetsPath = '/media/jasminb/ubuntu_data/Multi_label_learning/ProcessedDatasets/'

dataSetsNames = os.listdir(dataSetsPath)

numberOfSamples = 200  # control the number of points to perserve


def proba_mass_split(y, folds=3):
    obs, classes = y.shape
    dist = y.sum(axis=0).astype('float')
    dist /= dist.sum()
    index_list = []
    fold_dist = np.zeros((folds, classes), dtype='float')
    for _ in range(folds):
        index_list.append([])
    for i in range(obs):
        if i < folds:
            target_fold = i
        else:
            normed_folds = fold_dist.T / fold_dist.sum(axis=1)
            how_off = normed_folds.T - dist
            target_fold = np.argmin(np.dot((y[i] - .5).reshape(1, -1), how_off.T))
        fold_dist[target_fold] += y[i]
        index_list[target_fold].append(i)
    #print("Fold distributions are")
    #print(fold_dist)
    return index_list

def calculateIndecies(y_train):
    sentinel  = y_train.shape[0]
    print("At the first iteration is :", sentinel)
    if sentinel > int(numberOfSamples):
        while sentinel > numberOfSamples:
            q = proba_mass_split(y_train.values)
            kk = np.argmax([len(q[0]), len(q[1]), len(q[2])])
            y_train = y_train.iloc[q[kk], :]
            sentinel = y_train.shape[0]
            print("At this iteration is: ", sentinel)

    else:
        q = proba_mass_split(y_train.values)

    return q

errorDataSets = []

cnt = 0


for x in range(len(dataSetsNames)):
    dataset = dataSetsNames[x]
    readDataTrain = dataSetsPath + dataset+ "/" + dataset + "_train.arff"
    folderToStoreName = dataSetsPath + dataset + "/" + dataset + "_folds"

    #print("dataset count: {} and name: {} ".format(x+1, folderToStoreName + "/" + dataset + "train.arff"))
    print("#############")
    print(readDataTrain)
    print("#############")
    pom = True
    try:
        with open(readDataTrain, "r") as file1:
                train = arff.load(file1)

        targetIndex = int(train["relation"].rsplit(" ")[-1])

        #nTrain = pd.DataFrame(train["data"]).shape[0]
        #nTrain = min([nTrain, numberOfSamples])



        if targetIndex > 0:
            print("Na pochetok sum")

            X_train = pd.DataFrame(train["data"])
            y_train = X_train.iloc[:, :targetIndex].copy()
            for i in range(y_train.shape[1]):
                y_train.iloc[:, i] = y_train.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))
            y_train = y_train.astype("int32")

            indecies = calculateIndecies(y_train.copy())  # it returns list of indecies smaller than 1000
            print(len(indecies[0]))
            print(len(indecies[1]))
            print(len(indecies[2]))

            X_fold1 = X_train.iloc[indecies[0], :].copy()
            X_fold2 = X_train.iloc[indecies[1], :].copy()
            X_fold3 = X_train.iloc[indecies[2], :].copy()

            print(X_train.shape)
            c = X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0]
            print("C is", c)
            if X_train.shape[0] > 1000:
                v = 0
                while c < 1000:
                    inde = random.randint(0, X_train.shape[0])
                    print(inde)
                    if v == 0:
                        X_fold1 = X_fold1.append(pd.DataFrame(X_train.iloc[inde, :]).T, ignore_index=True)
                        v = v + 1
                        c = X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0]
                        continue
                    if v == 1:
                        X_fold2 = X_fold2.append(pd.DataFrame(X_train.iloc[inde, :]).T, ignore_index=True)
                        v = v + 1
                        c = X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0]
                        continue
                    if v == 2:
                        X_fold3 = X_fold3.append(pd.DataFrame(X_train.iloc[inde, :]).T, ignore_index=True)
                        v = 0
                        c = X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0]
                        continue

                #assert X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0] == 1000
            
            try:
                    print(folderToStoreName)
                    os.mkdir(folderToStoreName)
                    d = {}
                    d["data"] = sparse.coo_matrix(X_fold1)
                    d["attributes"] = train["attributes"]
                    d["relation"] = train["relation"]
                    d["description"] = train["description"]

                    with open(folderToStoreName + "/" + dataset + "fold1.arff", "w") as file1:
                        arff.dump(d, file1)

                    d = {}
                    d["data"] = sparse.coo_matrix(X_fold2)
                    d["attributes"] = train["attributes"]
                    d["relation"] = train["relation"]
                    d["description"] = train["description"]

                    with open(folderToStoreName + "/" + dataset + "fold2.arff", "w") as file1:
                        arff.dump(d, file1)

                    d = {}
                    d["data"] = sparse.coo_matrix(X_fold3)
                    d["attributes"] = train["attributes"]
                    d["relation"] = train["relation"]
                    d["description"] = train["description"]

                    with open(folderToStoreName + "/" + dataset + "fold3.arff", "w") as file1:
                        arff.dump(d, file1)
            except:
                os.rmdir(folderToStoreName)
                os.mkdir(folderToStoreName)
                d = {}
                d["data"] = sparse.coo_matrix(X_fold1)
                d["attributes"] = train["attributes"]
                d["relation"] = train["relation"]
                d["description"] = train["description"]

                with open(folderToStoreName + "/" + dataset + "fold1.arff", "w") as file1:
                    arff.dump(d, file1)

                d = {}
                d["data"] = sparse.coo_matrix(X_fold2)
                d["attributes"] = train["attributes"]
                d["relation"] = train["relation"]
                d["description"] = train["description"]

                with open(folderToStoreName + "/" + dataset + "fold2.arff", "w") as file1:
                    arff.dump(d, file1)

                d = {}
                d["data"] = sparse.coo_matrix(X_fold3)
                d["attributes"] = train["attributes"]
                d["relation"] = train["relation"]
                d["description"] = train["description"]

                with open(folderToStoreName + "/" + dataset + "fold3.arff", "w") as file1:
                    arff.dump(d, file1)
        else:
            print("Na kraj sum")
            X_train = pd.DataFrame(train["data"])
            y_train = X_train.iloc[:, targetIndex:].copy()

            for i in range(y_train.shape[1]):
                y_train.iloc[:, i] = y_train.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))

            y_train = y_train.astype("int32")
            indecies = calculateIndecies(y_train.copy())  # it returns list of indecies smaller than 1000

            print(len(indecies[0]))
            print(len(indecies[1]))
            print(len(indecies[2]))

            X_fold1 = X_train.iloc[indecies[0], :].copy()
            X_fold2 = X_train.iloc[indecies[1], :].copy()
            X_fold3 = X_train.iloc[indecies[2], :].copy()

            #print(X_train.shape)
            c = X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0]
            print("C is", c)
            if X_train.shape[0] > 1000:
                v = 0

                while c < 1000:
                    inde = random.randint(0, X_train.shape[0])
                    #print(inde)
                    #print(pd.DataFrame(X_train.iloc[inde, :]))
                    if v == 0:
                        X_fold1 = X_fold1.append(pd.DataFrame(X_train.iloc[inde, :]).T, ignore_index=True)
                        v = v + 1
                        c = X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0]
                        continue
                    if v == 1:
                        X_fold2 = X_fold2.append(pd.DataFrame(X_train.iloc[inde, :]).T, ignore_index=True)
                        v = v + 1
                        c = X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0]
                        continue
                    if v == 2:
                        X_fold3 = X_fold3.append(pd.DataFrame(X_train.iloc[inde, :]).T, ignore_index=True)
                        v = 0
                        c = X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0]
                        continue

               # assert X_fold1.shape[0] + X_fold2.shape[0] + X_fold3.shape[0] == 1000

            try:
                    os.mkdir(folderToStoreName)
                    d = {}
                    d["data"] = sparse.coo_matrix(X_fold1)
                    d["attributes"] = train["attributes"]
                    d["relation"] = train["relation"]
                    d["description"] = train["description"]

                    with open(folderToStoreName + "/" + dataset + "fold1.arff", "w") as file1:
                        arff.dump(d, file1)

                    d = {}
                    d["data"] = sparse.coo_matrix(X_fold2)
                    d["attributes"] = train["attributes"]
                    d["relation"] = train["relation"]
                    d["description"] = train["description"]

                    with open(folderToStoreName + "/" + dataset + "fold2.arff", "w") as file1:
                        arff.dump(d, file1)

                    d = {}
                    d["data"] = sparse.coo_matrix(X_fold3)
                    d["attributes"] = train["attributes"]
                    d["relation"] = train["relation"]
                    d["description"] = train["description"]

                    with open(folderToStoreName + "/" + dataset + "fold3.arff", "w") as file1:
                        arff.dump(d, file1)
            except:
                os.rmdir(folderToStoreName)
                os.mkdir(folderToStoreName)
                d = {}
                d["data"] = sparse.coo_matrix(X_fold1)
                d["attributes"] = train["attributes"]
                d["relation"] = train["relation"]
                d["description"] = train["description"]

                with open(folderToStoreName + "/" + dataset + "fold1.arff", "w") as file1:
                    arff.dump(d, file1)

                d = {}
                d["data"] = sparse.coo_matrix(X_fold2)
                d["attributes"] = train["attributes"]
                d["relation"] = train["relation"]
                d["description"] = train["description"]

                with open(folderToStoreName + "/" + dataset + "fold2.arff", "w") as file1:
                    arff.dump(d, file1)

                d = {}
                d["data"] = sparse.coo_matrix(X_fold3)
                d["attributes"] = train["attributes"]
                d["relation"] = train["relation"]
                d["description"] = train["description"]

                with open(folderToStoreName + "/" + dataset + "fold3.arff", "w") as file1:
                    arff.dump(d, file1)
    except:

        saveout = sys.stdout
        saveerr = sys.stderr
        logFile = open("out_"+dataset+".log", "w")
        sys.stdout = logFile
        print("The dataset " + dataset + " was not readed properly")
        errorFile = open("error_"+dataset+".log", "w")
        sys.stderr = errorFile
        print("The source of error for dataset " + dataset + " is: ", sys.stderr)
        sys.stdout = saveout
        sys.stderr = saveerr
        logFile.close()
        errorFile.close()
        print("########################################")
        print("FAULT IN READING THE DATA")
        print("########################################")
        errorDataSets.append(dataset)


