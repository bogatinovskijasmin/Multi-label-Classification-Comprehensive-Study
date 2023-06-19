"""
Input: MLL datasets.

This sorts all the files according to the metric: #features * #targets * #numberSamples.
It loads dataset by dataset. 
Supervisor adds the properties of each of the datasets.
The datasets should be in BigEndian format. The BigEndian refers that frist the target are present then the features in the .arff files.

Output: Sorted file containg the datasets in ascending order given the metric: #features * #targets * #numberSamples
"""
from  version_control_script import *

startTime = time()
def read_dataset(dataset_name):
    try:
        with open(dataset_name + "_train.arff", "r") as file1:
            train = arff.load(file1)


        with open(dataset_name + "_test.arff", "r") as file:
            test = arff.load(file)

    except:
        saveout = sys.stdout
        saveerr = sys.stderr
        logFile = open("out_"+dataset_name+".log", "w")
        sys.stdout = logFile
        print("The dataset " + dataset_name + " was not readed properly")
        errorFile = open("error_"+dataset_name+".log", "w")
        sys.stderr = errorFile
        print("The source of error for dataset " + dataset_name + " is: ", sys.stderr)
        sys.stdout = saveout
        sys.stderr = saveerr
        logFile.close()
        errorFile.close()
        print("Fail")
        return 1



    targetIndex = int(train["relation"].rsplit(" ")[-1])
    nTrain = pd.DataFrame(train["data"]).shape[0]
    nTest = pd.DataFrame(test["data"]).shape[0]

    if targetIndex > 0:
        print("Na pochetok sum")
        X_train = pd.DataFrame(train["data"])
        y_train = X_train.iloc[:nTrain, :targetIndex].copy()
        for i in range(y_train.shape[1]):
            y_train.iloc[:, i] = y_train.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))
        y_train = y_train.astype("int32")
        y_train = y_train.values
        X_train = X_train.iloc[:nTrain, targetIndex:].astype("float32")
        X_train = X_train.values
        X_test = pd.DataFrame(test["data"])
        y_test = X_test.iloc[:nTest, :targetIndex].copy()
        for i in range(y_test.shape[1]):
            y_test.iloc[:, i] = y_test.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))
        y_test = y_test.astype("int32")
        y_test = y_test.values
        X_test = X_test.iloc[:nTest, targetIndex:].astype("float32")
        X_test = X_test.values
    else:
        print("Na kraj sum")
        X_train = pd.DataFrame(train["data"])
        y_train = X_train.iloc[:nTrain, targetIndex:].copy()
        for i in range(y_train.shape[1]):
            y_train.iloc[:, i] = y_train.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))

        y_train = y_train.astype("int32")
        y_train = y_train.values
        X_train = X_train.iloc[:nTrain, :targetIndex].astype("float32")
        X_train = X_train.values

        X_test = pd.DataFrame(test["data"])

        y_test = X_test.iloc[:nTest, targetIndex:].copy()
        for i in range(y_test.shape[1]):
            y_test.iloc[:, i] = y_test.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))

        y_test = y_test.astype("int32")
        y_test = y_test.values
        X_test = X_test.iloc[:nTest, :targetIndex].astype("float32")
        X_test = X_test.values

    return [X_train, X_test, y_train, y_test, targetIndex]

def read_dataset_samples(dataset_name, numberOfSamples):
    try:
        with open(dataset_name + "_train.arff", "r") as file1:
            train = arff.load(file1)


        with open(dataset_name + "_test.arff", "r") as file:
            test = arff.load(file)

    except:
        saveout = sys.stdout
        saveerr = sys.stderr
        logFile = open("out_"+dataset_name+".log", "w")
        sys.stdout = logFile
        print("The dataset " + dataset_name + " was not readed properly")
        errorFile = open("error_"+dataset_name+".log", "w")
        sys.stderr = errorFile
        print("The source of error for dataset " + dataset_name + " is: ", sys.stderr)
        sys.stdout = saveout
        sys.stderr = saveerr
        logFile.close()
        errorFile.close()
        print("########################################")
        print("FAULT IN READING THE DATA")
        print("########################################")
        return 1



    targetIndex = int(train["relation"].rsplit(" ")[-1])


    nTrain = pd.DataFrame(train["data"]).shape[0]
    nTrain = min([nTrain, numberOfSamples])
    nTest = pd.DataFrame(test["data"]).shape[0]

    if targetIndex > 0:
        print("Na pochetok sum")
        X_train = pd.DataFrame(train["data"])
        X_train = X_train.sample(n=nTrain, random_state=setSeed)
        y_train = X_train.iloc[:nTrain, :targetIndex].copy()
        for i in range(y_train.shape[1]):
            y_train.iloc[:, i] = y_train.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))
        y_train = y_train.astype("int32")
        y_train = y_train.values
        X_train = X_train.iloc[:nTrain, targetIndex:].astype("float32")
        X_train = X_train.values
        X_test = pd.DataFrame(test["data"])
        y_test = X_test.iloc[:nTest, :targetIndex].copy()
        for i in range(y_test.shape[1]):
            y_test.iloc[:, i] = y_test.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))
        y_test = y_test.astype("int32")
        y_test = y_test.values
        X_test = X_test.iloc[:nTest, targetIndex:].astype("float32")
        X_test = X_test.values
    else:
        print("Na kraj sum")
        X_train = pd.DataFrame(train["data"])
        X_train = X_train.sample(n=nTrain, random_state=setSeed)
        y_train = X_train.iloc[:nTrain, targetIndex:].copy()
        for i in range(y_train.shape[1]):
            y_train.iloc[:, i] = y_train.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))

        y_train = y_train.astype("int32")
        y_train = y_train.values
        X_train = X_train.iloc[:nTrain, :targetIndex].astype("float32")
        X_train = X_train.values

        X_test = pd.DataFrame(test["data"])

        y_test = X_test.iloc[:nTest, targetIndex:].copy()
        for i in range(y_test.shape[1]):
            y_test.iloc[:, i] = y_test.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))

        y_test = y_test.astype("int32")
        y_test = y_test.values
        X_test = X_test.iloc[:nTest, :targetIndex].astype("float32")
        X_test = X_test.values

    return [X_train, X_test, y_train, y_test, targetIndex]


def read_dataset_fold(dataset_name, number):
    print(dataset_name)
    try:
        with open(dataset_name + "fold" + str(number) + ".arff", "r") as file1:
            train = arff.load(file1)

    except:
        saveout = sys.stdout
        saveerr = sys.stderr
        logFile = open("out_"+dataset_name+".log", "w")
        sys.stdout = logFile
        print("The dataset " + dataset_name + " was not readed properly")
        errorFile = open("error_"+dataset_name+".log", "w")
        sys.stderr = errorFile
        print("The source of error for dataset " + dataset_name + " is: ", sys.stderr)
        sys.stdout = saveout
        sys.stderr = saveerr
        logFile.close()
        errorFile.close()
        print("Fail")
        return 1

    targetIndex = int(train["relation"].rsplit(" ")[-1])
    nTrain = pd.DataFrame(train["data"]).shape[0]

    if targetIndex > 0:
        print("Na pochetok sum")
        X_train = pd.DataFrame(train["data"])
        y_train = X_train.iloc[:nTrain, :targetIndex].copy()
        for i in range(y_train.shape[1]):
            y_train.iloc[:, i] = y_train.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))
        y_train = y_train.astype("int32")
        y_train = y_train.values
        X_train = X_train.iloc[:nTrain, targetIndex:].astype("float32")
        X_train = X_train.values
    else:
        print("Na kraj sum")
        X_train = pd.DataFrame(train["data"])
        y_train = X_train.iloc[:nTrain, targetIndex:].copy()
        for i in range(y_train.shape[1]):
            y_train.iloc[:, i] = y_train.iloc[:, i].apply(lambda x: int(str(x).rsplit(".")[0]))

        y_train = y_train.astype("int32")
        y_train = y_train.values
        X_train = X_train.iloc[:nTrain, :targetIndex].astype("float32")
        X_train = X_train.values

    return [X_train, y_train, targetIndex]