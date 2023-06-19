from version_control_script import *
from dataSetsPreprocessing import *
from algorithmConfiguration import *
from evaluation_script import *

dataSetName = sys.argv[1]                            # the name od the dataset. For example: 'birds', 'Arabic1000', 'enron' etc.

print("##########################")
print(dataSetName)
print("##########################")



methodName = sys.argv[2]                             # Stores the method that is run
evalProcedure = sys.argv[3]                          # Stores the evalProcedure. Can be either "test" or "val"

if evalProcedure == "val":

    folderToStoreName = dataSetsPath + dataSetName + "/" + dataSetName + "_folds/"
    fold1 = read_dataset_fold(folderToStoreName + dataSetName, 1)                        # first index is the feature space, second index is the target space, 3th index is the targetIndex
    print("Successful read fold 1")
    fold2 = read_dataset_fold(folderToStoreName + dataSetName, 2)                        # first index is the feature space, second index is the target space, 3th index is the targetIndex
    print("Successful read fold 2")
    fold3 = read_dataset_fold(folderToStoreName + dataSetName, 3)                        # first index is the feature space, second index is the target space, 3th index is the targetIndex
    print("Successful read fold 3")


    if methodName == 'CLR':
        subsetCLR = {"C": [2], "G": [0.1, 0.1]}
        configurations = CalibratedLabelRanking(subsetCLR)

    if methodName == 'ECC':
        subsetECC = {"C": [2], "G":[0.1, 0.1], "I":[5]}
        configurations = EnsembleOfClassifierChains(subsetECC)

    if methodName == 'EBR':
        subsetEBR = {"C": [2], "G":[0.1, 0.1], "I":[5]}
        configurations = EnsembleOfBinaryRelevance(subsetEBR)

    if methodName == 'ELP':
        subsetELP = {"C": [2], "G":[0.1, 0.1], "I":[5]}
        configurations = EnsembleOfLabelPowerSets(subsetELP)

    if methodName == 'MBR':
        subsetMBR = {"C": [2], "G": [0.1, 0.1]}
        configurations = MetaBinaryRelevance(subsetMBR)

    if methodName == 'BR':
        subsetBR = {"C": [2, 4, 5, 4], "G":[0.1, 0.1]}
        configurations = BinaryRelevance(subsetBR)

    if methodName == 'LP':
        subsetLP = {"C": [2], "G":[0.1, 0.1]}
        configurations = LabelPowerSet(subsetLP)

    if methodName == 'PS':
        subsetPS = {"P": [1, 2], "M": [3], "N": [2]}
        configurations = PrunedSets(subsetPS)

    if methodName == 'EPS':
        subsetEPS = {"P": [1,2], "I":[3], "N":[2]}
        configurations = EnsembleOFPrunedSets(subsetEPS)

    tf1 = pd.DataFrame(fold1[0])
    tf2 = pd.DataFrame(fold2[0])
    tf3 = pd.DataFrame(fold3[0])

    tar1 = pd.DataFrame(fold1[1])
    tar2 = pd.DataFrame(fold2[1])
    tar3 = pd.DataFrame(fold3[1])

    descriptiveIter1 = pd.concat([tf1, tf2], axis=0).values
    descriptiveIter2 = pd.concat([tf1, tf3], axis=0).values
    descriptiveIter3 = pd.concat([tf2, tf3], axis=0).values

    targetIter1 = pd.concat([tar1, tar2], axis=0).values
    targetIter2 = pd.concat([tar1, tar3], axis=0).values
    targetIter3 = pd.concat([tar2, tar3], axis=0).values

    print("Test shape: ", fold1[0].shape)
    print("Train shape: ", descriptiveIter1.shape)
    print(type(fold1[0]))

    for x in range(len(configurations)):
        pickRandomConfig = random.randint(0, len(configurations))
        clf = configurations[pickRandomConfig][0]
        fileName1 = dataSetName + "_" + configurations[pickRandomConfig][1] + "_fold3_predictions"
        fileName2 = dataSetName + configurations[pickRandomConfig][1] + "_fold2_predictions"
        fileName3 = dataSetName + "_" + configurations[pickRandomConfig][1] + "_fold1_predictions"

        try:
            #fold1 eval
            clf.fit(descriptiveIter1, targetIter1)
            pred1 = clf.predict(fold3[0])

            print(fileName1)
            q1 = Evaluation(clf,dataSetName, fileName1, y_test=fold3[1], pred=pred1, y_score=None)

        except:
            saveout = sys.stdout
            saveerr = sys.stderr
            logFile = open("out_" + fileName1 + ".log", "w")
            sys.stdout = logFile
            print("The " + fileName1 + " was not evaluated")
            errorFile = open("error_" + fileName1 + ".log", "w")
            sys.stderr = errorFile
            print("The source of error for evaluation " + fileName1 + " is: ", sys.stderr)
            sys.stdout = saveout
            sys.stderr = saveerr
            logFile.close()
            errorFile.close()

        #fold2 eval
        try:
            clf.fit(descriptiveIter2, targetIter2)
            pred2 = clf.predict(fold2[0])

            q2 = Evaluation(clf,dataSetName, fileName2, y_test=fold2[1], pred=pred2, y_score=None)
        except:
            saveout = sys.stdout
            saveerr = sys.stderr
            logFile = open("out_" + fileName2 + ".log", "w")
            sys.stdout = logFile
            print("The " + fileName2 + " was not evaluated")
            errorFile = open("error_" + fileName2 + ".log", "w")
            sys.stderr = errorFile
            print("The source of error for evaluation " + fileName2 + " is: ", sys.stderr)
            sys.stdout = saveout
            sys.stderr = saveerr
            logFile.close()
            errorFile.close()


        #fold3 eval
        try:
            clf.fit(descriptiveIter3, targetIter3)
            pred3 = clf.predict(fold1[0])
            q3 = Evaluation(clf,dataSetName, fileName3, y_test=fold1[1], pred=pred3, y_score=None)
        except:
            saveout = sys.stdout
            saveerr = sys.stderr
            logFile = open("out_" + fileName3 + ".log", "w")
            sys.stdout = logFile
            print("The " + fileName3 + " was not evaluated")
            errorFile = open("error_" + fileName3 + ".log", "w")
            sys.stderr = errorFile
            print("The source of error for evaluation " + fileName3 + " is: ", sys.stderr)
            sys.stdout = saveout
            sys.stderr = saveerr
            logFile.close()
            errorFile.close()
        exit("Finish one iteration")

if evalProcedure == "test":
    folderToStoreName = dataSetsPath + dataSetName + "/" + dataSetName
    data = read_dataset(folderToStoreName)  # read the data; returns list of 5 elements being: X_train, X_test, y_train, y_test
    X_train = data[0]  # contains the train feature set for dataSetName
    X_test = data[1]  # contains the test set for dataSetName
    y_train = data[2]  # contains the train label set for dataSetName
    y_test = data[3]  # contains the test set for dataSetName
    targetIndex = data[4]  # contains the index of the begining of the target label set in dataSetName.
    ####### Can be >0 or <0. If >0  the labels are in begining of arff file. If <0 the labels are at the end of the MEKA file.


    if methodName == 'CLR':
        subsetCLR = {"C": [2], "G": [0.1, 0.1]}
        configurations = CalibratedLabelRanking(subsetCLR)

    if methodName == 'ECC':
        subsetECC = {"C": [2], "G":[0.1, 0.1], "I":[5]}
        configurations = EnsembleOfClassifierChains(subsetECC)

    if methodName == 'EBR':
        subsetEBR = {"C": [2], "G":[0.1, 0.1], "I":[5]}
        configurations = EnsembleOfBinaryRelevance(subsetEBR)

    if methodName == 'ELP':
        subsetELP = {"C": [2], "G":[0.1, 0.1], "I":[5]}
        configurations = EnsembleOfLabelPowerSets(subsetELP)

    if methodName == 'MBR':
        subsetMBR = {"C": [2], "G": [0.1, 0.1]}
        configurations = MetaBinaryRelevance(subsetMBR)

    if methodName == 'BR':
        subsetBR = {"C": [2], "G":[0.1, 0.1]}
        configurations = BinaryRelevance(subsetBR)

    if methodName == 'LP':
        subsetLP = {"C": [2], "G":[0.1, 0.1]}
        configurations = LabelPowerSet(subsetLP)

    if methodName == 'PS':
        subsetPS = {"P": [1, 2], "M": [3], "N": [2]}
        configurations = PrunedSets(subsetPS)

    if methodName == 'EPS':
        subsetEPS = {"P": [1,2], "I":[3], "N":[2]}
        configurations = EnsembleOFPrunedSets(subsetEPS)

    clf = configurations[0][0]

    clf.fit(X_train, y_train)
    print("Finished training\n")

    pred = clf.predict(X_test)
    print("Finished prediction\n")
    print(type(X_test))

    filename = dataSetName + "_" + configurations[0][1] + "_test_predictions"

    q = Evaluation(clf, dataSetName, filename, y_test, pred, y_score=None)
    print("Finished evaluation")

if q==0:
    print("Successful execution")