from version_control_script import *
from dataSetsPreprocessing import *
from algorithmConfiguration import *


def Evaluation(clf, dataSetName, filename, y_test, pred, y_score=None):
    outputDictionary = {}
    #outputDictionary["LABEL RANKING LOSS"] = label_ranking_loss(y_true=y_test, y_score=prob)
    #outputDictionary["LABEL RANKING AVERAGE PRECISION"] = label_ranking_average_precision_score(y_true=y_test,y_score=prob)
    #outputDictionary["COVARAGE"] = coverage_error(y_true=y_test,y_score=prob)
    #outputDictionary["AUCROC"] = roc_auc_score(y_true=y_test,y_score=prob)
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
    outputDictionary["The configuration is"] = clf.meka_classifier + " " + clf.weka_classifier
    outputDictionary["The model name"] = filename

    with open(dataSetName + filename + ".json", "w") as outFile:
            json.dump(outputDictionary, outFile)

    print("Successfull Evaluation")
    return 0