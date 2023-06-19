from version_control_script import *
from dataSetsPreprocessing import *
from algorithmConfiguration import *
from evaluation_script import *
import time


# dataSetName = sys.argv[1]                            # the name od the dataset. For example: 'birds', 'Arabic1000', 'enron' etc.

dataSetName = "ABPM"
evalProcedure = "val"



methodName = "CLR"



timeForExecution = 1000

print("##########################")
print(dataSetName)
print("##########################")

print("##########################")
print(methodName)
print("##########################")


def checkLabelsWithZeros(y_true, prediction, y_scores):
    trueLabels = pd.DataFrame(y_true)
    predLabels = pd.DataFrame(prediction)
    y_sc = pd.DataFrame(y_scores)

    pre = trueLabels.shape[0]

    trueLabels["sum"] = trueLabels.sum(axis=1)
    predLabels["sum"] = predLabels.sum(axis=1)

    trueLabels.loc[:, "sum"] = np.where(trueLabels.loc[:, "sum"] == 0, 1, 0)
    predLabels.loc[:, "sum"] = np.where(predLabels.loc[:, "sum"] == 0, 1, 0)

    trueLabels.loc[:, "sum"] += predLabels.loc[:, "sum"].values
    predLabels.loc[:, "sum"] += trueLabels.loc[:, "sum"].values

    trueLabels = trueLabels[trueLabels.loc[:, "sum"] != 1]
    predLabels = predLabels[predLabels.loc[:, "sum"] != 1]

    trueLabels = trueLabels.drop(["sum"], axis=1)
    predLabels = predLabels.drop(["sum"], axis=1)

    y_sc  = y_sc.iloc[trueLabels.index, :].values



    post = trueLabels.shape[0]

    numberRemoved = abs(pre - post)

    return [trueLabels.values, predLabels.values, y_sc, numberRemoved]

def storeModel(clf, fileName):
    try:
        print("I have entred the save model function")
        filename = 'finalized_model.sav'
        pickle.dump(clf, open(fileName, 'wb'))
        print("Successfull_store_the_model: ", fileName)

    except:
        print("The model {} failed to be stored".format(fileName))




#for methodName in ["MLTSVM", "RAkEL", "RSMLCC", "RSMLLC", "CLR", "EBR", "ECC", "ELP", "EPS", "BPNN", "HOMER", "CDN", "MBR", "BR", "MLKNN", "CLEMS", "MLARM", "BRkNN"]:
for methodName in ["BR"]:
    if evalProcedure == "val":

        folderToStoreName = dataSetsPath + dataSetName + "/" + dataSetName + "_folds/"
        fold1 = read_dataset_fold(folderToStoreName + dataSetName, 1)  # first index is the feature space, second index is the target space, 3th index is the targetIndex
        print("Successful read fold 1")
        fold2 = read_dataset_fold(folderToStoreName + dataSetName, 2)  # first index is the feature space, second index is the target space, 3th index is the targetIndex
        print("Successful read fold 2")
        fold3 = read_dataset_fold(folderToStoreName + dataSetName, 3)  # first index is the feature space, second index is the target space, 3th index is the targetIndex
        print("Successful read fold 3")

        targetIndex = abs(fold1[-1])

        numberEnsembleMembers = min(50, 2 * np.abs(targetIndex))

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

        maxNumberNeurons = np.max([descriptiveIter1.shape[0], descriptiveIter2.shape[0], descriptiveIter3.shape[0]])

        if methodName == 'CLR':
            subsetCLR = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)]}
            configurations = CalibratedLabelRanking(subsetCLR)

        if methodName == "ECC":
            subsetECC = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)],
                         "I": [10, numberEnsembleMembers]}
            configurations = EnsembleOfClassifierChains(subsetECC)

        if methodName == "MBR":
            subsetMBR = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)]}
            configurations = MetaBinaryRelevance(subsetMBR)

        if methodName == "EBR":
            subsetEBR = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)],
                         "I": [10, numberEnsembleMembers]}
            configurations = EnsembleOfBinaryRelevance(subsetEBR)

        if methodName == "ELP":
            subsetELP = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)],
                         "I": [10, numberEnsembleMembers]}
            configurations = EnsembleOfLabelPowerSets(subsetELP)

        if methodName == "EPS":
            subsetEPS = {"P": [1, 2, 3], "I": [10, numberEnsembleMembers], "N": [0, 3]}
            configurations = EnsembleOFPrunedSets(subsetEPS)

        if methodName == "BR":
            subsetBR = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)]}
            configurations = BinaryRelevance(subsetBR)

        if methodName == "CC":
            subsetCC = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)]}
            configurations = ClassifierChains(subsetCC)

        if methodName == "LP":
            subsetLP = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)]}
            configurations = LabelPowerSet(subsetLP)

        if methodName == "PS":
            subsetPS = {"P": [1, 2, 3], "M": [2], "N": [0,
                                                        3]}  # for N it is recommended if the cardinality of the labels are greater than 2 to be 0
            configurations = PrunedSets(subsetPS)

        if methodName == "RAkEL":
            subsetRAkEL = {"cost": [2 ** j for j in range(-5, 15, 2)], "gamma": [2 ** j for j in range(-15, 3, 2)],
                           "labelSubspaceSize": [3, abs(int(targetIndex / 2))], "pruningValue": [1]}
            configurations = RAkEL_MEKA(subsetRAkEL, targetIndex)

        if methodName == "BPNN":
            subsetBPNN = {
                "hidden": [int(maxNumberNeurons * 0.2), int(maxNumberNeurons * 0.25), int(maxNumberNeurons * 0.15)],
                "epoches": [200], "learningRate": [0.01, 0.1]}  # see paper on MLTSVM
            configurations = BackPropagationNeuralNetwork(subsetBPNN)

        if methodName == 'MLTSVM':
            subsetMLTSVM = {"cost": [2 ** j for j in range(-6, 6, 1)],
                            "lambda_param": [2 ** j for j in range(-4, 4, 1)],
                            "smootParam": [1, 0.1, 1.5]}  # as recommended in their paper
            configurations = TwinMultiLabelSVM(subsetMLTSVM)

        if methodName == "MLARM":
            subsetMLARM = {"vigilance": [0.8, 0.9, 0.85, 0.95], "threshold": [0.02, 0.0001, 0.05]}
            configurations = MultilabelARAM(subsetMLARM)

        if methodName == "MLkNN":
            subsetMLkNN = {"k": [6, 8, 10, 12, 14, 16, 18, 20]}
            configurations = MLkNearestNeighbour(subsetMLkNN)

        if methodName == "BRkNN":
            subsetBRkNN = {"k": [6, 8, 10, 12, 14, 16, 18, 20]}
            configurations = BRkNearestNeighbour(subsetBRkNN)

        if methodName == "CLEMS":
            subsetCLEMS = {"k": [6, 10, 12, 16, 18]}
            configurations = CostSensitiveLabelEmbedding(subsetCLEMS)

        if methodName == "RSMLCC":
            subsetRandomSubspacesCC = {"iterations": [10, numberEnsembleMembers], "attributes": [25, 50, 75]}
            configurations = RandomSubspaces_CC(subsetRandomSubspacesCC)

        if methodName == "RSMLLC":
            subsetRandomSubspacesLC = {"iterations": [10, numberEnsembleMembers], "attributes": [25, 50, 75]}
            configurations = RandomSubspaces_LP(subsetRandomSubspacesLC)

        if methodName == "HOMER":
            subsetHOMER = {"clusters": [2, 3, 4, 5, 6], "cost": [2 ** j for j in range(-5, 15, 2)],
                           "gamma": [2 ** j for j in range(-15, 3, 2)]}
            configurations = HierarchyOMER(subsetHOMER)

        if methodName == "CDN":
            subsetCDN = {"I": [250, 500, 750], "Ic": [25, 50, 75]}
            configurations = ConditionalDependencyNetwork(subsetCDN)

        if methodName == "SSM":
            configurations = SubSetMapper()

        majorTime = 0
        lenConfig = len(configurations)
        s = lenConfig - 1
        for x in range(lenConfig):
            print("###################################################################################")
            print("###################################################################################")
            print("STARTING ", methodName)
            print("###################################################################################")
            print("###################################################################################")


            print("s is up: ", s)
            if s == 0:
                pickRandomConfig = 0
                print("Tuka vlegov samo ednshka")
                setExit = True
            else:

                pickRandomConfig = random.randint(0, s)   # To exclude eventually occurance of the last out of range configuration
                print(pickRandomConfig)
                if pickRandomConfig >= s:
                    pickRandomConfig = pickRandomConfig -1

                print("Pop element: ", pickRandomConfig)
                configurations.pop(pickRandomConfig)

            print("{} configurations to evaluate".format(s))
            s = s - 1


            clf = configurations[pickRandomConfig][0]
            fileName1 = dataSetName + "_" + configurations[pickRandomConfig][1].replace("_", " ") + "_fold3_predictions"
            fileName2 = dataSetName + "_" + configurations[pickRandomConfig][1].replace("_", " ") + "_fold2_predictions"
            fileName3 = dataSetName + "_" + configurations[pickRandomConfig][1].replace("_", " ") + "_fold1_predictions"



            try:
                fold1TimeCounterStart = time.time()
                clf.fit(descriptiveIter1, targetIter1)
                print("Processing dataset {} for configuration {}".format(dataSetName, configurations[pickRandomConfig][1].replace("_", " ") + "_fold3_predictions"))

                pred1 = clf.predict(fold3[0])


                if methodName in ["RAkEL", "RSMLCC", "RSMLLC"]:
                    #this methods provides votes
                    y_scores1 = np.array(clf.probabilites_)

                if methodName in ["LP", "CC", "PS", "SSM"]:
                    # this methods provide predictions. They do not provide ranking.
                    y_scores1 = np.array(pred1)

                if methodName in ["MLTSVM"]:
                #    # this method provide predictions it is pythonish. Doesn't provide scores.
                    y_scores1 = pred1

                if methodName in ["MLKNN", "CLEMS"]:
                    #provide probs in sparse format. We fix it to give
                    y_scores1 = np.array(clf.predict_proba(fold3[0]).todense())

                if methodName in ["MLARM"]:
                    #this method provides probabilites in dense format
                    y_scores1 = np.array(clf.predict_proba(fold3[0]))

                if methodName in ["CLR", "EBR", "ECC", "ELP", "EPS", "BPNN", "HOMER", "CDN", "MBR", "BR"]:
                    y_scores1 = np.array(clf.probabilites_)

                if methodName == "BRkNN":
                    y_scores1 = np.array(clf.confidences_)


                endTimeFold1 = time.time() - fold1TimeCounterStart
                majorTime += endTimeFold1


                if majorTime > timeForExecution:
                    print("The time for evaluation has expired")
                    break

                #storeModel(clf, fileName1)

            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open("out_" + fileName1 + ".log", "w")
                sys.stdout = logFile
                print("###################################################################################")
                print("###################################################################################")
                print("The " + fileName1 + " was not evaluated.\n")
                print("###################################################################################")
                print("The source of error for evaluation " + fileName1.replace("_", " ") + " is: ", sys.stderr)
                print("###################################################################################")
                print("###################################################################################")
                sys.stdout = saveout
                sys.stderr = saveerr
                logFile.close()


            #fold2 eval
            try:
                fold2TimeCounterStart = time.time()
                clf.fit(descriptiveIter2, targetIter2)
                print("Processing dataset {} for configuration {}".format(dataSetName, configurations[pickRandomConfig][1].replace("_", " ") + "_fold2_predictions"))

                pred2 = clf.predict(fold2[0])



                if methodName in ["RAkEL", "RSMLCC", "RSMLLC"]:
                    # this methods provides votes
                    y_scores2 = np.array(clf.probabilites_)

                if methodName in ["LP", "CC", "PS", "SSM"]:
                    # this methods provide predictions. They do not provide ranking.
                    y_scores2 = np.array(pred2)

                if methodName in ["MLTSVM"]:
                    #    # this method provide predictions it is pythonish. Doesn't provide scores.
                    y_scores2 = pred2

                if methodName in ["MLKNN", "CLEMS"]:
                    # provide probs in sparse format. We fix it to give
                    y_scores2 = np.array(clf.predict_proba(fold2[0]).todense())

                if methodName in ["MLARM"]:
                    # this method provides probabilites in dense format
                    y_scores2 = np.array(clf.predict_proba(fold2[0]))

                if methodName in ["CLR", "EBR", "ECC", "ELP", "EPS", "BPNN", "HOMER", "CDN", "MBR", "BR"]:
                    y_scores2 = np.array(clf.probabilites_)

                if methodName == "BRkNN":
                    y_scores2 = np.array(clf.confidences_)



                endTimeFold2 = time.time() - fold2TimeCounterStart
                majorTime += endTimeFold2

                if majorTime > timeForExecution:
                    print("The time for evaluation has expired")
                    break

                #storeModel(clf, fileName2)

            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open("out_" + fileName2 + ".log", "w")
                sys.stdout = logFile
                print("The " + fileName2 + " was not evaluated")
                print("###################################################################################")
                print("###################################################################################")
                print("The " + fileName2 + " was not evaluated.\n")
                print("###################################################################################")
                print("The source of error for evaluation " + fileName2.replace("_", " ") + " is: ", sys.stderr)
                print("###################################################################################")
                print("###################################################################################")
                print("The source of error for evaluation " + fileName2.replace("_", " ") + " is: ", sys.stderr)
                sys.stdout = saveout
                sys.stderr = saveerr
                logFile.close()

            #fold3 eval
            try:
                fold3TimeCounterStart = time.time()
                clf.fit(descriptiveIter3, targetIter3)
                print("Processing dataset {} for configuration {}".format(dataSetName, configurations[pickRandomConfig][1].replace("_", " ") + "_fold1_predictions"))

                pred3 = clf.predict(fold1[0])


                if methodName in ["RAkEL", "RSMLCC", "RSMLLC"]:
                    # this methods provides votes
                    y_scores3 = np.array(clf.probabilites_)

                if methodName in ["LP", "CC", "PS", "SSM"]:
                    # this methods provide predictions. They do not provide ranking.
                    y_scores3 = np.array(pred3)

                if methodName in ["MLTSVM"]:
                    #    # this method provide predictions it is pythonish. Doesn't provide scores.
                    y_scores3 = pred3

                if methodName in ["MLKNN", "CLEMS"]:
                    # provide probs in sparse format. We fix it to give
                    y_scores3 = np.array(clf.predict_proba(fold1[0]).todense())

                if methodName in ["MLARM"]:
                    # this method provides probabilites in dense format
                    y_scores3 = np.array(clf.predict_proba(fold1[0]))

                if methodName in ["CLR", "EBR", "ECC", "ELP", "EPS", "BPNN", "HOMER", "CDN", "MBR", "BR"]:
                    y_scores3 = np.array(clf.probabilites_)

                if methodName == "BRkNN":
                    y_scores3 = np.array(clf.confidences_)





                endTimeFold3 = time.time() - fold3TimeCounterStart
                majorTime += endTimeFold3

                if majorTime > timeForExecution:
                    print("The time for evaluation has expired")
                    break

                #storeModel(clf, fileName3)



            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open("out_" + fileName3 + ".log", "w")
                sys.stdout = logFile
                print("The " + fileName3 + " was not evaluated")
                print("###################################################################################")
                print("###################################################################################")
                print("The " + fileName3 + " was not evaluated.\n")
                print("###################################################################################")
                print("The source of error for evaluation " + fileName3.replace("_", " ") + " is: ", sys.stderr)
                print("###################################################################################")
                print("###################################################################################")
                sys.stdout = saveout
                sys.stderr = saveerr
                logFile.close()


            print("PERFORMING DATA TYPES COMPARISON AND ACCOMODATION")
            if type(pred1) != type(fold3[0]):
                pred1 = pred1.todense()

            if type(pred2) != type(fold2[0]):
                pred2 = pred2.todense()

            if type(pred3) != type(fold1[0]):
                pred3 = pred3.todense()


            if type(y_scores1) != type(fold3[0]):
                y_scores1 = y_scores1.todense()

            if type(y_scores2) != type(fold2[0]):
                y_scores2 = y_scores2.todense()

            if type(y_scores3) != type(fold1[0]):
                y_scores3 = y_scores3.todense()

            #print("TRANSFOMRING LABELS SUCH THAT THERE ARE NO 0 VALUES FOR PRECISION RECALL AND F-SCORE")
            #filterTarget1 = checkLabelsWithZeros(fold3[1], pred1, y_scores1)
            #filterTarget2 = checkLabelsWithZeros(fold2[1], pred2, y_scores2)
            #filterTarget3 = checkLabelsWithZeros(fold1[1], pred3, y_scores3)


            print("CALCULATING EVALUATION MEASURES\n")



            #q1 = Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName1.replace(" ", "_"), y_test=filterTarget1[0], pred=filterTarget1[1], y_score=filterTarget1[2], x=x, removedValues=filterTarget1[3], timeForEval=endTimeFold1)

            #q2 = Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName2.replace(" ", "_"), y_test=filterTarget2[0], pred=filterTarget2[1], y_score=filterTarget2[2], x=x, removedValues=filterTarget2[3], timeForEval=endTimeFold2)

            #q3 = Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName3.replace(" ", "_"), y_test=filterTarget3[0], pred=filterTarget3[1], y_score=filterTarget3[2], x=x, removedValues=filterTarget3[3], timeForEval=endTimeFold3)

            q1 = Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName1.replace(" ", "_"), y_test=fold3[1], pred=pred1, y_score=y_scores1, x=x, removedValues=3, timeForEval=endTimeFold1)
            q2 = Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName2.replace(" ", "_"), y_test=fold2[1], pred=pred2, y_score=y_scores2, x=x, removedValues=3, timeForEval=endTimeFold2)
            q3 = Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName3.replace(" ", "_"), y_test=fold1[1], pred=pred3, y_score=y_scores3, x=x, removedValues=3, timeForEval=endTimeFold3)

            print("The time executed for now is: ", majorTime)
            time.sleep(5)
            print("DONE method: ", methodName)
            break

