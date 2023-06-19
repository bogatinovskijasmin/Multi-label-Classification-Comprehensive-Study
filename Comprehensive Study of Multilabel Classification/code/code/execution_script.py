from version_control_script import *
from dataSetsPreprocessing import *
from algorithmConfiguration import *
from evaluation_script import *
import time


#dataSetName = sys.argv[1]                            # the name od the dataset. For example: 'birds', 'Arabic1000', 'enron' etc.
#methodName = sys.argv[2]                             # Stores the method that is run
#evalProcedure = sys.argv[3]                          # Stores the evalProcedure. Can be either "test" or "val"

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
        print("Successfull_store_the_model: ",fileName)

    except:
        print("The model {} failed to be stored".format(fileName))


def standardizeData(train, fnames, test):


    from sklearn.preprocessing import MinMaxScaler
    from scipy import sparse as sss
    for x in range(train.shape[1]):
        if "real" or "numeric" in fnames[x]:
            mm = MinMaxScaler()
            train[:, x] = mm.fit_transform(train[:, x].reshape(-1, 1)).reshape((train.shape[0], ))
            test.iloc[:,x] = mm.transform(test.iloc[:, x].values.reshape(-1, 1)).reshape((test.shape[0], ))

    return train, test



def usage():
    process = psutil.Process(os.getpid())
    return process.memory_info()[0]/float(2**20)


def download_data(dataSetName, timeToWait, numberOfAttempts):
    """

    :param dataSetName: name of the structure folder you want to download
    :param timeToWait: how much time do you want to wait. This is multipled with the number of attempts you want to try
    :param numberOfAttempts: how many times will you reattempt
    :return:
    """
    try:

        destination = currentDir +"/" + "ProcessedDatasets/" + dataSetName + "/" + dataSetName + "_folds/"
        print("#######################################")
        print(destination)
        print("#######################################")

        os.makedirs(destination)
        print("#######################################")
        print(destination)
        print("#######################################")


        shutil.copy2(dataSetName+"fold1.arff", destination)
        shutil.copy2(dataSetName + "fold2.arff", destination)
        shutil.copy2(dataSetName + "fold3.arff", destination)
        time.sleep(40)
        return True
    except:
        print("can't make folders")
        return False

    #for x in range(numberOfAttempts):
    #    destination = placeData + dataSetName+"/"+dataSetName+"_folds/"
        #source = "gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/" + dataSetName+"/"+dataSetName+"_folds/"
        #try:
        #    os.system("arccp " + source + " " + destination)
        #    print("###################################################\n")
        #    print("The data are being downloaded!!!")
        #    print("###################################################\n")

        #except:
        #    print("###################################################\n")
        #    print("Attempt {} was not successfull!!!!".format(numberOfAttempts))
        #    time.sleep(timeToWait)
        #    print("###################################################\n")

    #downladedFiles = os.listdir(destination)

    #cnt = 0

    #for pom in range(len(downladedFiles)):
    #    file = pom+1
    #    if dataSetName+"fold"+str(file)+".arff" in downladedFiles:
    #        cnt = cnt + 1

    #if cnt==3:
    #    print("###################################################\n")
    #    print("The data was downloaded!!!")
    #    print("###################################################\n")
    #    return True
    #elif cnt > 0:
    #    print("###################################################\n")
    #    print("The data was paritally downloaded!!!")
    #    print("###################################################\n")
    #    return False
    #else:
    #    print("###################################################\n")
    #    print("The data has not been downloaded.")
    #    print("###################################################\n")
    #    return False


def findBestTreshold(scores, y_test):
    # this function finds the best threshold such that label cardinality of test and pred are as close as possibkle
    trainCardi = label_cardinality(y_test)
    bestCard = 10000.0
    for th in list(np.arange(0.0015, 1, 0.05)):
        pom = np.where(scores > th, 1.0, 0.0)
        testCardin  = label_cardinality(pom)
        if np.abs(testCardin - trainCardi) < bestCard:
            print("Test cardinality: ", testCardin)
            print("Train cardinality: ", trainCardi)
            bestCard = np.abs(testCardin - trainCardi)
            bestTh = th

    pred = np.where(scores > bestTh, 1.0, 0.0)
    return pred


def EvaluationFuntion(dataSetName, methodName, evalProcedure, timeForExecution):
    setExit = False

    if evalProcedure == "val":
        folderToStoreName = dataSetsPath + dataSetName + "/" + dataSetName + "_folds/"
        print("###################################################\n")
        print("I read data from: ", folderToStoreName)
        print("###################################################\n")

        # SECTION 1
        ################################################################################################################################
        print("###################################################\n")
        print("####### START DATASET READING FUNCTION INFORMATIONS #########\n")
        fold1 = read_dataset_fold(folderToStoreName + dataSetName, 1)
        print("###################################################\n")
        print("Successful read fold 1\n")
        print("###################################################\n")
        fold2 = read_dataset_fold(folderToStoreName + dataSetName, 2)
        print("###################################################\n")
        print("Successful read fold 2\n")
        print("###################################################\n")
        fold3 = read_dataset_fold(folderToStoreName + dataSetName, 3)                        # first index is the feature space, second index is the target space, 3th index is the targetIndex. SAME FOR ALL 3
        print("###################################################\n")
        print("Successful read fold 3\n")
        print("###################################################\n")                        # READ THE DATA

        print("####### END DATASET READING FUNCTION INFORMATIONS #########\n")
        print("###################################################\n")
        ################################################################################################################################

        # SECTION 2
        ################################################################################################################################
        targetIndex = abs(fold1[2])
        numberEnsembleMembers = min(50, 2 * (np.abs(targetIndex)))                             # Some of the parameters of the methods are depended on the number of labels. Store the number of labels
        ################################################################################################################################

        featuresNames = fold1[3]
        sparse = fold1[4]

        # SECTION 3
        ################################################################################################################################
        tf1 = pd.DataFrame(fold1[0])
        tf2 = pd.DataFrame(fold2[0])
        tf3 = pd.DataFrame(fold3[0])

        tar1 = pd.DataFrame(fold1[1])
        tar2 = pd.DataFrame(fold2[1])
        tar3 = pd.DataFrame(fold3[1])                                                        # CREATE DATA FRAMES FOR BETTER MANIPULATION WITH THE DATA

        ################################################################################################################################

        print("###################################################\n")
        print("MEMORY USAGE AFTER CREATING THE DATA FRAMES ", usage())
        print("###################################################\n")


        # SECTION 4
        ############################################################################################################################
        descriptiveIter1 = pd.concat([tf1, tf2], axis=0).values
        descriptiveIter2 = pd.concat([tf1, tf3], axis=0).values
        descriptiveIter3 = pd.concat([tf2, tf3], axis=0).values

        descriptiveIter1, tf3 = standardizeData(descriptiveIter1, fnames=featuresNames, test=tf3)
        descriptiveIter2, tf2 = standardizeData(descriptiveIter2, fnames=featuresNames, test=tf2)
        descriptiveIter3, tf1 = standardizeData(descriptiveIter3, fnames=featuresNames, test=tf1)


        targetIter1 = pd.concat([tar1, tar2], axis=0).values
        targetIter2 = pd.concat([tar1, tar3], axis=0).values
        targetIter3 = pd.concat([tar2, tar3], axis=0).values                                 # CREATE THE TRAINING DATASETS
        ############################################################################################################################

        print("###################################################\n")
        print("MEMORY USAGE AFTER CREATING THE DATA FRAME FOLDS ", usage())
        print("###################################################\n")

        # SECTION 5   # free memory
        ############################################################################################################################

        del tf1
        del tf2
        del tf3

        del tar1
        del tar2
        del tar3

        print("###################################################\n")
        print("MEMORY USAGE AFTER DELETING POM VARIABLES ", usage())
        print("###################################################\n")

        ############################################################################################################################




        maxNumberNeurons = np.max([descriptiveIter1.shape[1], descriptiveIter2.shape[1], descriptiveIter3.shape[1]])   # PARAMETERS FOR BPMLL




        # SECTION 6                                                                            PARAMETARIZATION OF THE ALGORTIHMS
        ############################################################################################################################

        if methodName == 'CLR':
            subsetCLR = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)]}
            configurations = CalibratedLabelRanking(subsetCLR)

        if methodName == "ECC":
            subsetECC = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)],
                         "I": [10]}
            configurations = EnsembleOfClassifierChains(subsetECC)

        if methodName == "MBR":
            subsetMBR = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)]}
            configurations = MetaBinaryRelevance(subsetMBR)

        if methodName == "EBR":
            subsetEBR = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)],
                         "I": [10]}
            configurations = EnsembleOfBinaryRelevance(subsetEBR)

        if methodName == "ELP":
            subsetELP = {"C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)],
                         "I": [10]}
            configurations = EnsembleOfLabelPowerSets(subsetELP)

        if methodName == "EPS":
            subsetEPS = {"P": [1, 2, 3], "I": [10], "N": [0, 3]}
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

        if methodName == "PSt":
            subsetPS = {"P": [1, 2, 3],  "N": [0, 3], "C": [2 ** j for j in range(-5, 15, 2)], "G": [2 ** j for j in range(-15, 3, 2)]}  # for N it is recommended if the cardinality of the labels are greater than 2 to be 0
            configurations = PrunedSets(subsetPS)

        if methodName == "RAkEL1":
            #MULAN implememtation
            subsetRAkEL1 = {"cost": [2 ** j for j in range(-5, 15, 2)], "gamma": [2 ** j for j in range(-15, 3, 2)]}
            configurations = RAkEL1(subsetRAkEL1, targetIndex)


        if methodName == "RAkEL2":
            # MekaImplementation
            subsetRAkEL2 = {"cost": [2 ** j for j in range(-5, 15, 2)], "gamma": [2 ** j for j in range(-15, 3, 2)],"labelSubspaceSize":[3, abs(int(targetIndex/2))], "pruningValue":[1]}
            configurations = RAkEL2(subsetRAkEL2, targetIndex)

        if methodName == "BPNN":
            subsetBPNN = {
                "hidden": [int(maxNumberNeurons * 0.2), int(maxNumberNeurons * 0.25), int(maxNumberNeurons * 0.15)],
                "epoches": [200], "learningRate": [0.01, 0.1]}  # see paper on MLTSVM
            configurations = BackPropagationNeuralNetwork(subsetBPNN)

        if methodName == 'MLTSVM':
            subsetMLTSVM = {"cost": [2 ** j for j in range(-6, 6, 1)],
                            "lambda_param": [2 ** j for j in range(-4, 4, 1)],
                            "smootParam": [1, 0.2],
                            }  # as recommended in their paper
            configurations = TwinMultiLabelSVM(subsetMLTSVM)

        if methodName == "MLARM":
            subsetMLARM = {"vigilance": [0.8, 0.9, 0.85, 0.95],
                           "threshold": [0.02, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.0001, 0.05]}
            configurations = MultilabelARAM(subsetMLARM)

        if methodName == "MLkNN":
            subsetMLkNN = {"k": [6, 8, 10, 12, 14, 16, 18, 20]}
            configurations = MLkNearestNeighbour(subsetMLkNN)

        if methodName == "BRkNN":
            subsetBRkNN = {"k": [6, 8, 10, 12, 14, 16, 18, 20]}
            configurations = BRkNearestNeighbour(subsetBRkNN)

        if methodName == "CLEMS":
            subsetCLEMS = {"k": [6, 8, 10, 12, 14, 16, 18, 20]}
            configurations = CostSensitiveLabelEmbedding(subsetCLEMS)

        if methodName == "RSMLCC":
            subsetRandomSubspacesCC = {"iterations": [10, numberEnsembleMembers], "attributes": [25, 50, 75], "confidence":[0.001, 0.01, 0.1, 0.2, 0.25, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]}
            configurations = RandomSubspaces_CC(subsetRandomSubspacesCC)

        if methodName == "RSMLLC":
            subsetRandomSubspacesLC = {"iterations": [10, numberEnsembleMembers], "attributes": [25, 50, 75], "cost": [2 ** j for j in range(-5, 15, 2)], "gamma": [2 ** j for j in range(-15, 3, 2)]}
            configurations = RandomSubspaces_LP(subsetRandomSubspacesLC)

        if methodName == "HOMER":
            if np.abs(targetIndex) < 5:
                clList = [2, 3]
            elif np.abs(targetIndex) < 6:
                clList = [2, 3, 4]
            elif np.abs(targetIndex) < 7:
                clList = [2, 3, 4, 5]
            else:
                clList = [2, 3, 4, 5, 6]


            subsetHOMER = {"clusters": clList, "cost": [2 ** j for j in range(-5, 15, 2)],
                           "gamma": [2 ** j for j in range(-15, 3, 2)]}
            configurations = HierarchyOMER(subsetHOMER)

        if methodName == "CDN":
            subsetCDN = {"I": [250, 500, 750], "Ic": [25, 50, 75]}
            configurations = ConditionalDependencyNetwork(subsetCDN)

        if methodName == "SSM":
            configurations = SubSetMapper()


        if methodName == "LINE":
            subsetLCCB = {"k":[6, 10, 12, 16, 18]}
            configurations = OpenNetworkEmbedder(setOfParamters=subsetLCCB, targetIndex=np.abs(targetIndex))


        ############################################################################################################################


        majorTime = 0
        lenConfig = len(configurations)

        print(len(configurations))
        d = {}
        for x in range(lenConfig):
            d[methodName] = x

            if len(configurations) == 1:
                pickRandomConfig = 0
                print("###################################################################################\n")
                print("LAST CONFIGURATION TO EXECUTE")
                print("###################################################################################\n")
                setExit = True
            else:
                pickRandomConfig = random.randint(0, len(configurations)-1)   # To exclude eventually occurance of the last out of range configuration
                print("###################################################################################\n")
                print("The chosen configuration index is: ", pickRandomConfig)
                print("###################################################################################\n")


            print("###################################################################################\n")
            print("{} more configurations to evaluate!!".format(len(configurations)))
            print("###################################################################################\n")

            clf = configurations[pickRandomConfig][0]


            fileName1 = dataSetName + "_" + configurations[pickRandomConfig][1].replace(".", "__") + "_fold3_predictions"
            fileName2 = dataSetName + "_" + configurations[pickRandomConfig][1].replace(".", "__") + "_fold2_predictions"
            fileName3 = dataSetName + "_" + configurations[pickRandomConfig][1].replace(".", "__") + "_fold1_predictions"



            try:
                fold1TimeCounterStart = time.time()
                clf.fit(descriptiveIter1, targetIter1)
                print("###################################################################################\n")
                print("Processing dataset {} for configuration {}".format(dataSetName, configurations[pickRandomConfig][1].replace("_", " ") + " fold3 predictions"))
                print("###################################################################################\n")

                pred1 = clf.predict(fold3[0])


                if methodName in ["RAkEL2", "RSMLCC", "RSMLLC"]:
                    #this methods provides votes
                    y_scores1 = np.array(clf.probabilites_)
                    #pred1 = np.array(pred1)

                if methodName in [ "LP", "CC", "SSM"]:
                    # this methods provide predictions. They do not provide ranking.
                    y_scores1 = np.array(clf.probabilites_)

                if methodName in ["MLTSVM"]:
                #    # this method provide predictions it is pythonish. Doesn't provide scores.
                    y_scores1 = pred1

                if methodName in ["MLkNN", "CLEMS", "LINE"]:
                    #provide probs in sparse format. We fix it to give numpy.
                    y_scores1 = np.array(clf.predict_proba(fold3[0]).todense())


                if methodName in ["MLARM"]:
                    #this method provides probabilites in dense format
                    y_scores1 = np.array(clf.predict_proba(fold3[0]))

                if methodName in ["CLR", "EBR", "ECC", "ELP", "EPS", "BPNN", "HOMER", "CDN", "MBR", "BR", "PSt", "RAkEL1"]:
                    y_scores1 = np.array(clf.probabilites_)
                    #pred1 = np.array(pred1)

                if methodName == "BRkNN":
                    y_scores1 = np.array(clf.confidences_)

                endTimeFold1 = time.time() - fold1TimeCounterStart
                majorTime += endTimeFold1

                #if endTimeFold1 > int(timeForExecution / 3)  and int(timeForExecution) <15000:
                #    continue

                print(y_scores1)
                print("############################")
                print(pred1)

                print("############################")
                print(fold3[1])


                print("###################################################################################\n")
                print("###################################################################################\n")
                print("EXECUTION TIME: ", majorTime)
                print("###################################################################################\n")
                print("###################################################################################\n")


                if majorTime >= timeForExecution:
                    print("###################################################################################\n")
                    print("The time for evaluation has expired!!!")
                    print("EXITING THE EVALUATION PROCEDURE!!!")
                    print("###################################################################################\n")
                    break

                #storeModel(clf, fileName1)

            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open(fileName1 + "_out_.log", "w")
                sys.stdout = logFile
                print("###################################################################################\n")
                print("###################################################################################\n")
                print("The " + fileName1 + " was not evaluated.\n")
                print("###################################################################################\n")
                print("The source of error for evaluation " + fileName1.replace("_", " ") + " is: \n", sys.stderr)
                print("###################################################################################\n")
                print("###################################################################################\n")
                sys.stdout = saveout
                sys.stderr = saveerr
                logFile.close()

            #fold2 eval
            try:
                fold2TimeCounterStart = time.time()
                clf.fit(descriptiveIter2, targetIter2)
                print("###################################################################################\n")
                print("Processing dataset {} for configuration {}".format(dataSetName, configurations[pickRandomConfig][1].replace("_", " ") + " fold2 predictions"))
                print("###################################################################################\n")

                pred2 = clf.predict(fold2[0])

                if methodName in ["RAkEL2", "RSMLCC", "RSMLLC"]:
                    # this methods provides votes
                    y_scores2 = np.array(clf.probabilites_)
                    #pred2 = np.array(pred2)

                if methodName in ["LP", "CC",  "SSM"]:
                    # this methods provide predictions. They do not provide ranking.
                    y_scores2 = np.array(clf.probabilites_)

                if methodName in ["MLTSVM"]:
                    #    # this method provide predictions it is pythonish. Doesn't provide scores.
                    y_scores2 = pred2

                if methodName in ["MLkNN", "CLEMS", "LINE"]:
                    # provide probs in sparse format. We fix it to give
                    y_scores2 = np.array(clf.predict_proba(fold2[0]).todense())

                if methodName in ["MLARM"]:
                    # this method provides probabilites in dense format
                    y_scores2 = np.array(clf.predict_proba(fold2[0]))

                if methodName in ["CLR", "EBR", "ECC", "ELP", "EPS", "BPNN", "HOMER", "CDN", "MBR", "BR", "PSt", "RAkEL1"]:
                    y_scores2 = np.array(clf.probabilites_)
                    #pred2 = np.array(pred2)

                if methodName == "BRkNN":
                    y_scores2 = np.array(clf.confidences_)


                endTimeFold2 = time.time() - fold2TimeCounterStart
                majorTime += endTimeFold2

               # if endTimeFold2 > int(timeForExecution / 3) and int(timeForExecution) <15000:
                #    continue


                print("###################################################################################\n")
                print("###################################################################################\n")
                print("EXECUTION TIME: ", majorTime)
                print("###################################################################################\n")
                print("###################################################################################\n")
                if majorTime > timeForExecution:
                    print("###################################################################################\n")
                    print("The time for evaluation has expired!!!")
                    print("EXITING THE EVALUATION PROCEDURE!!!")
                    print("###################################################################################\n")
                    break

                #storeModel(clf, fileName2)

            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open(fileName2 + "_out_.log", "w")
                sys.stdout = logFile
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
                print("Processing dataset {} for configuration {}".format(dataSetName, configurations[pickRandomConfig][1].replace("_", " ") + " fold1 predictions"))

                pred3 = clf.predict(fold1[0])

                if methodName in ["RAkEL2", "RSMLCC", "RSMLLC"]:
                    # this methods provides votes
                    y_scores3 = np.array(clf.probabilites_)
                    #pred3 = np.array(pred3)

                if methodName in ["LP", "CC", "SSM"]:
                    # this methods provide predictions. They do not provide ranking.
                    y_scores3 = np.array(clf.probabilites_)

                if methodName in ["MLTSVM"]:
                    #    # this method provide predictions it is pythonish. Doesn't provide scores.
                    y_scores3 = pred3

                if methodName in ["MLkNN", "CLEMS", "LINE"]:
                    # provide probs in sparse format. We fix it to give
                    y_scores3 = np.array(clf.predict_proba(fold1[0]).todense())

                if methodName in ["MLARM"]:
                    # this method provides probabilites in dense format
                    y_scores3 = np.array(clf.predict_proba(fold1[0]))

                if methodName in ["CLR", "EBR", "ECC", "ELP", "EPS", "BPNN", "HOMER", "CDN", "MBR", "BR", "PSt", "RAkEL1"]:
                    y_scores3 = np.array(clf.probabilites_)
                    #pred3 = np.array(pred3)


                if methodName == "BRkNN":
                    y_scores3 = np.array(clf.confidences_)


                endTimeFold3 = time.time() - fold3TimeCounterStart
                majorTime += endTimeFold3


                print("###################################################################################\n")
                print("###################################################################################\n")
                print("EXECUTION TIME: ", majorTime)
                print("###################################################################################\n")
                print("###################################################################################\n")



                if majorTime > timeForExecution:
                    print("###################################################################################\n")
                    print("The time for evaluation has expired!!!")
                    print("EXITING THE EVALUATION PROCEDURE!!!")
                    print("###################################################################################\n")
                    break

                #storeModel(clf, fileName3)



            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open(fileName3 + "_out_.log", "w")
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

            print("###################################################################################\n")
            print("###################################################################################\n")
            print("PERFORMING DATA TYPES COMPARISON AND ACCOMODATION")
            print("###################################################################################\n")
            print("###################################################################################\n")



            #print("########################################")
            #print(methodName)
            #print("########################################")
            #print("########################################")
            #print(y_scores1.shape)
            #print(fold3[1].shape)
            #print("########################################")
            #print(y_scores2.shape)
            #print(fold2[1].shape)
            #print("########################################")
            #print(y_scores3.shape)
            #print(fold1[1].shape)
            #print("########################################")
            #print("########################################")

            #time.sleep(5)
            #break


            #if type(pred1) != type(fold3[0]):
            #    if "matrix" in str(type(pred1)):
            #        print("the type of pred 1 is matrix\n")
            #    else:
            #        pred1 = pred1.todense()

            #if type(pred2) != type(fold2[0]):
            #    if "matrix" in str(type(pred2)):
            #        print("the type of pred 2 is matrix\n")
            #    else:
            #        pred2 = pred2.todense()


            #if type(pred3) != type(fold1[0]):
            #    if "matrix" in str(type(pred3)):
            #        print("the type of pred 3 is matrix\n")
            #    else:
            #        pred3 = pred3.todense()


            if type(y_scores1) != type(fold3[0]):
                if "matrix" in str(type(y_scores1)):
                    print("the type of y_scores1 is matrix\n")
                else:
                    y_scores1 = y_scores1.todense()


            if type(y_scores2) != type(fold2[0]):
                if "matrix" in str(type(y_scores2)):
                    print("the type of y_scores2 is matrix\n")
                else:
                    y_scores2 = y_scores2.todense()

            if type(y_scores3) != type(fold1[0]):
                if "matrix" in str(type(y_scores3)):
                    print("the type of y_scores3 is matrix\n")
                else:
                    y_scores3 = y_scores3.todense()

            # if methodName in ["EBR", "ECC", "ELP", "EPS"]:
            #    y_scores1 = np.divide(y_scores1, iter)



            if methodName in ["RSMLCC"]:
                y_scores1 = np.divide(y_scores1, np.max(y_scores1))
                y_scores2 = np.divide(y_scores2, np.max(y_scores2))
                y_scores3 = np.divide(y_scores3, np.max(y_scores3))

            if methodName in ["RAkEL2"]:
                y_scores1 = np.divide(y_scores1, np.max(y_scores1))
                y_scores2 = np.divide(y_scores2, np.max(y_scores2))
                y_scores3 = np.divide(y_scores3, np.max(y_scores3))

            if methodName in ["MLARM"]:
                y_scores1 = np.divide(y_scores1, np.max(y_scores1))
                y_scores2 = np.divide(y_scores2, np.max(y_scores2))
                y_scores3 = np.divide(y_scores3, np.max(y_scores3))

            if methodName in ["TREMLC"]:
                y_scores1 = np.divide(y_scores1, np.max(y_scores1))
                y_scores2 = np.divide(y_scores2, np.max(y_scores2))
                y_scores3 = np.divide(y_scores3, np.max(y_scores3))

            if methodName in ["TREMLCnew"]:
                y_scores1 = np.divide(y_scores1, np.max(y_scores1))
                y_scores2 = np.divide(y_scores2, np.max(y_scores2))
                y_scores3 = np.divide(y_scores3, np.max(y_scores3))

            pred1 = findBestTreshold(y_scores1, fold3[1])
            pred2 = findBestTreshold(y_scores2, fold2[1])
            pred3 = findBestTreshold(y_scores3, fold1[1])

            if methodName in ["MLTSVM", "LP", "CC", "SSM"]:
                print("#############\n")
                print("DO not provide score.\n")
                print("#############\n")
                t1 = 0
                t2 = 0
                t3 = 0
                t4 = 0
            else:
                t1 = time.time()
                pred1 = findBestTreshold(y_scores1, fold3[1])
                t2 = time.time()
                pred2 = findBestTreshold(y_scores2, fold2[1])
                t3 = time.time()
                pred3 = findBestTreshold(y_scores3, fold1[1])
                t4 = time.time()


            tfold1 = t2 - t1
            tfold2 = t3 - t2
            tfold3 = t4 - t3


            print(y_scores1)
            print("############################")
            print(pred1)

            print("############################")
            print(fold3[1])


            #print("TRANSFOMRING LABELS SUCH THAT THERE ARE NO 0 VALUES FOR PRECISION RECALL AND F-SCORE")
            #filterTarget1 = checkLabelsWithZeros(fold3[1], pred1, y_scores1)
            #filterTarget2 = checkLabelsWithZeros(fold2[1], pred2, y_scores2)
            #filterTarget3 = checkLabelsWithZeros(fold1[1], pred3, y_scores3)

            print("###################################################################################\n")
            print("CALCULATING EVALUATION MEASURES\n")
            print("###################################################################################\n")

            try:
                Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName1.replace(" ", "_").replace(".", "__"), y_test=fold3[1], pred=pred1, y_score=y_scores1, x=x, removedValues="NaN", timeForEval=endTimeFold1 + tfold1, methodName = methodName)
            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open(fileName1 +  "_evaluation_error_.log", "w")
                sys.stdout = logFile
                print("The " + fileName1 + " was not evaluated")
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
            try:
                Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName2.replace(" ", "_").replace(".", "__"), y_test=fold2[1], pred=pred2, y_score=y_scores2, x=x, removedValues="NaN", timeForEval=endTimeFold2 + tfold2, methodName=methodName)
            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open(fileName2 +  "_evaluation_error_.log", "w")
                sys.stdout = logFile
                print("The " + fileName2 + " was not evaluated")
                print("###################################################################################")
                print("###################################################################################")
                print("The " + fileName2 + " was not evaluated.\n")
                print("###################################################################################")
                print("The source of error for evaluation " + fileName2.replace("_", " ") + " is: ", sys.stderr)
                print("###################################################################################")
                print("###################################################################################")
                sys.stdout = saveout
                sys.stderr = saveerr
                logFile.close()
            try:
                Evaluation(configurations[pickRandomConfig][2], dataSetName, fileName3.replace(" ", "_").replace(".", "__"), y_test=fold1[1], pred=pred3, y_score=y_scores3, x=x, removedValues="NaN", timeForEval=endTimeFold3 + tfold3, methodName=methodName)
            except:
                saveout = sys.stdout
                saveerr = sys.stderr
                logFile = open(fileName3 +  "_evaluation_error_.log", "w")
                sys.stdout = logFile
                print("The " + fileName3 + " was not evaluated")
                print("###################################################################################\n")
                print("###################################################################################\n")
                print("The " + fileName3 + " was not evaluated.\n")
                print("###################################################################################")
                print("The source of error for evaluation " + fileName3.replace("_", " ") + " is: ", sys.stderr)
                print("###################################################################################\n")
                print("###################################################################################\n")
                sys.stdout = saveout
                sys.stderr = saveerr
                logFile.close()

            print("###################################################################################\n")
            print("###################################################################################\n")
            print("###################################################################################\n")
            print("###################################################################################\n")
            print("THE ELAPSED TIME IS: {} sec. \n".format(majorTime))
            print("###################################################################################\n")
            print("###################################################################################\n")
            print("###################################################################################\n")
            print("###################################################################################\n")


            if setExit == True:
                print("###################################################################################\n")
                print("###################################################################################\n")
                print("###################################################################################\n")
                print("###################################################################################\n")
                print("ALL MODELS ARE EVALUATED")
                print("###################################################################################\n")
                print("###################################################################################\n")
                print("###################################################################################\n")
                print("###################################################################################\n")
            del configurations[pickRandomConfig]

            #break


    if evalProcedure == "test":
        """
        THIS PART OF THE SCRIPT IS TO MAKE THE TEST PREDICTIONS !!! 
        """
        print("Finished evaluation")



if __name__ == '__main__':

    dataSetName = sys.argv[1]
    evalProcedure = sys.argv[3]
    methodName = sys.argv[2]

    #dataSetName = "ML_SPIRIT"
    #evalProcedure = "val"
    #methodName = "BR"
    timeForExecution = 43200
   #timeForExecution = 43200
    numberOfAttemptsToDownload = 500
    timeToWaitIfDownloadPerAttemptIsNotSuccessful = 60 #in seconds

    toProceed = download_data(dataSetName=dataSetName, timeToWait=timeToWaitIfDownloadPerAttemptIsNotSuccessful, numberOfAttempts=numberOfAttemptsToDownload)
    #toProceed = True
    #for methodName in ["MLTSVM", "RAkEL1", "RAkEL2", "LINE", "RSMLCC", "RSMLLC", "CLR", "EBR", "ECC", "ELP", "EPS", "PSt", "BPNN", "HOMER", "CDN", "MBR", "BR", "MLkNN", "CLEMS", "MLARM", "BRkNN", "SSM", "LP", "CC"]:
    #for methodName in ["CLR"]:
    #    print("##########################\n")
    #    print(dataSetName)
    #    print("##########################\n")
    #    print("##########################\n")
    #    print(methodName)
    #    print("##########################\n")
    #    EvaluationFuntion(dataSetName, methodName, evalProcedure, timeForExecution)
    #EvaluationFuntion(dataSetName=dataSetName, methodName=methodName, evalProcedure=evalProcedure, timeForExecution=timeForExecution)
    #toProceed = True
#THIS IS FUNCTIONAL CODE DO NOT DELETE !!!
    if toProceed == True:
        #for methodName in ["MLTSVM", "RAkEL2", "RSMLCC",  "CLR", "EBR", "ECC", "ELP", "EPS", "PSt", "BPNN", "HOMER", "CDN", "MBR", "BR", "MLkNN", "CLEMS", "MLARM", "SSM", "LP", "CC"]:
        #for methodName in ["MLTSVM", "RAkEL2", "RSMLCC", "CLR", "EBR", "ECC", "ELP", "EPS", "PSt", "BPNN", "HOMER",
        #                   "CDN", "MBR", "BR", "MLkNN", "CLEMS", "MLARM", "SSM", "LP", "CC"]:
        #for methodName in ["EBR", "ELP", "ECC"]:
        #for methodName in ["CC"]:
            print("##########################\n")
            print(dataSetName)
            print("##########################\n")
            print("##########################\n")
            print(methodName)
            print("##########################\n")
            EvaluationFuntion(dataSetName, methodName, evalProcedure, timeForExecution)
            time.sleep(10)  # this is to provide enough time for storage
    else:
        saveout = sys.stdout
        saveerr = sys.stderr
        logFile = open(dataSetName+ "_" + methodName +"_download_error_.log", "w")
        sys.stdout = logFile
        print("The " + dataSetName + " couldn't have been downloaded after {} seconds".format(numberOfAttemptsToDownload*timeToWaitIfDownloadPerAttemptIsNotSuccessful))
        print("###################################################################################\n")
        print("###################################################################################\n")
        print("PLEASE TRY LATER AGAIN\n")
        print("###################################################################################\n")
        print("###################################################################################\n")
        sys.stdout = saveout
        sys.stderr = saveerr
        logFile.close()
