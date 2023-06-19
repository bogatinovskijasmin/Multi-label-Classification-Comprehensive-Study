from  version_control_script import *
from dataSetsPreprocessing import *
from algorithmConfiguration import *
from evaluation_script import *


startTime = time()

dataSetName = "yeast"
nTrain = 1000                                        # max number of instances for dataSetName to perserve
data = read_dataset_samples(dataSetName, nTrain)     # read the data; returns list of 5 elements being: X_train, X_test, y_train, y_test
X_train = data[0]                                    # contains the train feature set for dataSetName
X_test = data[1].copy()                              # contains the test set for dataSetName
y_train = data[2]                                    # contains the train label set for dataSetName
y_test = data[3]                                     # contains the test set for dataSetName
targetIndex = data[4]                                # contains the index of the begining of the target label set in dataSetName.
                                                     ####### Can be >0 or <0. If >0  the labels are in begining of arff file. If <0 the labels are at the end of the MEKA file.


folderToStoreName = dataSetsPath + dataSetName + "/" + dataSetName + "_folds/"
fold1 = read_dataset_fold(folderToStoreName+dataSetName, 1)

X_train = fold1[0].copy()
y_train = fold1[1].copy()
targetIndex = fold1[2]

numberEnsembleMembers = min(30, 2*np.abs(targetIndex))

subsetCLR = {"C": [ 2**j for j in range(-5, 15, 2) ], "G":[ 2**j for j in range(-15, 3, 2) ]}
subsetECC = {"C": [ 2**j for j in range(-5, 15, 2) ], "G":[ 2**j for j in range(-15, 3, 2) ], "I":[10, numberEnsembleMembers]}
subsetMBR = {"C": [ 2**j for j in range(-5, 15, 2) ], "G":[ 2**j for j in range(-15, 3, 2) ]}
subsetEBR = {"C": [ 2**j for j in range(-5, 15, 2) ], "G":[ 2**j for j in range(-15, 3, 2) ], "I":[10, numberEnsembleMembers]}
subsetELP = {"C": [ 2**j for j in range(-5, 15, 2) ], "G":[ 2**j for j in range(-15, 3, 2) ], "I":[10, numberEnsembleMembers]}
subsetBR = {"C": [ 2**j for j in range(-5, 15, 2) ], "G":[ 2**j for j in range(-15, 3, 2) ]}
subsetCC = {"C": [ 2**j for j in range(-5, 15, 2) ], "G":[ 2**j for j in range(-15, 3, 2) ]}
subsetLP = {"C": [ 2**j for j in range(-5, 15, 2) ], "G":[ 2**j for j in range(-15, 3, 2) ]}
#subsetPS = {"P": [1, 2, 3], "M":[2], "N":[0, 3]}  # for N it is recommended if the cardinality of the labels are greater than 2 to be 0
subsetEPS = {"P": [1, 2, 3], "I":[10, numberEnsembleMembers], "N":[0, 3]}
subsetRAkEL = {"cost": [ 2**j for j in range(-5, 15, 2) ], "gamma":[ 2**j for j in range(-15, 3, 2) ], "labelSubspaceSize":[3, abs(int(targetIndex/2))], "pruningValue":[1]}
subsetBPNN = {"hidden":[int(X_train.shape[0]*0.2), int(X_train.shape[0]*0.25), int(X_train.shape[0]*0.15)], "epoches":[200],"learningRate":[0.01, 0.1] }   # see paper on MLTSVM
subsetMLTSVM = {"cost":[ 2**j for j in range(-8, 4, 2)], "lambda_param":[ 2**j for j in range(-8, 4, 2)], "smootParam":[ 2**j for j in range(-8, 4, 2) ]}
subsetMLARM = {"vigilance":[0.8, 0.9, 0.85, 0.95], "threshold":[0.02, 0.0001, 0.05]}
subsetMLkNN = {"k":[6, 8, 10, 12, 14, 16, 18, 20]}
subsetBRkNN = {"k":[6, 8, 10, 12, 14, 16, 18, 20]}
subsetCLEMS = {"k":[6, 10, 12, 16, 18]}
subsetRandomSubspacesCC = {"iterations":[10, numberEnsembleMembers], "attributes":[25, 50, 75]}
subsetRandomSubspacesLP = {"iterations":[10, numberEnsembleMembers], "attributes":[25, 50, 75]}
subsetHOMER = {"clusters":[2, 3, 4, 5, 6], "cost": [ 2**j for j in range(-5, 15, 2) ], "gamma":[ 2**j for j in range(-15, 3, 2) ]}
subsetCDN = {"I": [250, 500, 750], "Ic":[25, 50, 75]}
#subsetMLDNN = {"hidden":[int(X_train.shape[0]*0.2), int(X_train.shape[0]*0.25), int(X_train.shape[0]*0.15)], "epoches":[200],"learningRate":[0.01, 0.1] }   # see paper on MLTSVM
subsetLCCB = {"k":[6, 10, 12, 16, 18]}

CLR = CalibratedLabelRanking(subsetCLR)
ECC = EnsembleOfClassifierChains(subsetECC)
MBR = MetaBinaryRelevance(subsetMBR)
EBR = EnsembleOfBinaryRelevance(subsetEBR)
ELP = EnsembleOfLabelPowerSets(subsetELP)
BR = BinaryRelevance(subsetBR)
LP = LabelPowerSet(subsetLP)
#PS = PrunedSets(subsetPS)
EPS = EnsembleOFPrunedSets(subsetEPS)
RAKELMEKA = RAkEL_MEKA(subsetRAkEL, np.abs(targetIndex))
BPNN = BackPropagationNeuralNetwork(subsetBPNN)
CC = ClassifierChains(subsetCC)
MLTSVM = TwinMultiLabelSVM(subsetMLTSVM)   # doesn't provide probabilitites
MLARM = MultilabelARAM(subsetMLARM)        # provides ranking
MLKNN = MLkNearestNeighbour(subsetMLkNN)   # provides probabities, use todense
BRkNN = BRkNearestNeighbour(subsetBRkNN)   # provides confidences scores,
CLEMS = CostSensitiveLabelEmbedding(subsetCLEMS) # provides probabilites, use dense
#RSCC = RandomSubspaces_CC(subsetRandomSubspacesCC)
#RSLP = RandomSubspaces_LP(subsetRandomSubspacesLP)
HOMER = HierarchyOMER(subsetHOMER)
SSM = SubSetMapper()                      # this has no parameteres
CDN = ConditionalDependencyNetwork(subsetCDN)
LINE = OpenNetworkEmbedder(setOfParamters=subsetLCCB, targetIndex=np.abs(targetIndex))
# add PCT and MLC4.5
# add RFPCT and RFMLC4.5




#rakel = RAkEL(subsetRAkEL, np.abs(targetIndex))
#clusterer = RandomLabelSpaceClusterer(cluster_size=10, cluster_count=5, allow_overlap=True)
#clf = ens.RakelO(base_classifier=baseClfTree, model_count=int(2*np.abs(targetIndex)), labelset_size=3, base_classifier_require_dense=True)
#clf = ens.RakelD(base_classifier=baseClfTree, labelset_size=3, base_classifier_require_dense=False)
#clf = ens.MajorityVotingClassifier(classifier=baseClfTree, clusterer=clusterer)


"""
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

baseClfTree = DecisionTreeClassifier()
baseClfSVM = SVC(kernel="rbf", gamma=0.1, C=10)

clf  = prob_tras.BinaryRelevance(classifier=baseClfSVM, require_dense=True)
"""

clf = LINE[3][0]
y_train1 = y_train.copy()
clf.fit(X_train.copy(), y_train.copy())
print("##############")
#print(clf._error)
print("##############")

def CalculateThrashold(clf, y_train, X_test):
    m = label_cardinality(y_train)
    s = 0.0001
    prev = 0
    for th in np.arange(0.00001, 0.9999, 0.0005).tolist():
        clf.threshold = th
        trainCardinality = label_cardinality(y_train)
        y_test = clf.predict(X_test)
        testCardinality = label_cardinality(y_test)
        if m > np.abs(trainCardinality - testCardinality):
            m = np.abs(trainCardinality-testCardinality)
            s = th
        if np.round(testCardinality, 2) == np.round(trainCardinality, 2):
            return [s, clf]
        if y_test.sum() == prev:
            break
        prev = y_test.sum()
    return [s, clf]


#zz = CalculateThrashold(clf, y_train1, X_test)


#pred = zz[1].predict(X_test)
pred = clf.predict(X_test)
#prob = zz[1].predict_proba(X_test)
#prob = clf.confidences_
#prob = clf.probabilites_


#filename = dataSetName + clf.meka_classifier + " " + clf.weka_classifier + ".sav"
outputDictionary = {}
#outputDictionary["LABEL RANKING LOSS"] = label_ranking_loss(y_true=y_test, y_score=prob)
#outputDictionary["LABEL RANKING AVERAGE PRECISION"] = label_ranking_average_precision_score(y_true=y_test,y_score=prob)
#outputDictionary["COVARAGE"] = coverage_error(y_true=y_test,y_score=prob)
#outputDictionary["AUCROC"] = roc_auc_score(y_true=y_test, y_score=prob)
outputDictionary["HAMMING LOSS exampble based"] = hamming_loss(y_true=y_test, y_pred=pred)
outputDictionary["PRECISION example based"] = precision_score(y_true=y_test, y_pred=pred, average="samples")
outputDictionary["RECALL example based"] = recall_score(y_true=y_test, y_pred=pred, average="samples")
outputDictionary["F1 examplbe based"] = f1_score(y_true=y_test, y_pred=pred, average="samples")
outputDictionary["ACCURACY example-based"] = jaccard_similarity_score(y_true=y_test, y_pred=pred)
outputDictionary["SUBSET ACCURACY"] = accuracy_score(y_true=y_test, y_pred=pred)
outputDictionary["MACRO PRECISION"] = precision_score(y_true=y_test, y_pred=pred, average="macro")
outputDictionary["MICRO PRECISION"] = precision_score(y_true=y_test, y_pred=pred, average="micro")
outputDictionary["MACRO RECALL"] = recall_score(y_true=y_test, y_pred=pred, average="macro")
outputDictionary["MICRO RECALL"] = recall_score(y_true=y_test, y_pred=pred, average="micro")
outputDictionary["MACRO F1"] = f1_score(y_true=y_test, y_pred=pred, average="macro")
outputDictionary["MICRO F1"] = f1_score(y_true=y_test, y_pred=pred, average="micro")
#print("Statistics from MEKA: ", clf._statistics)
outputDictionary["The needed time is"] = time()-startTime
outputDictionary["The configuration is"] = MLARM[1][2]
outputDictionary["The model name"] = MLARM[1][1]


#Evaluation(clf, dataSetName, "aa", y_test, pred, prob)

with open(dataSetName+"results_1.json", "w") as outFile:
        json.dump(outputDictionary, outFile)

#pickle.dump(clf, open(filename, 'wb'))