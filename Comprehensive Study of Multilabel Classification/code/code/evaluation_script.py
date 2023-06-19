from version_control_script import *
from dataSetsPreprocessing import *
from algorithmConfiguration import *



def one_error(y_true, y_score):

    try:
        x = np.zeros_like(y_score)
        x[np.arange(y_score.shape[0]), y_score.argmax(1)] = 1
        z = np.multiply(y_true, x)
        res = z.sum(axis=1)
        res = np.where(res, 1, 0)
        res = res.sum() / y_true.shape[0]
    except:
        res = np.nan
    return res



def Evaluation(d, dataSetName, filename, y_test, pred, y_score, x, removedValues, timeForEval, methodName):
    outputDictionary = {}

    try:
        outputDictionary["LABEL RANKING LOSS"] = label_ranking_loss(y_true=y_test, y_score=y_score)
    except:
        outputDictionary["LABEL RANKING LOSS"] = str(np.nan)
    try:
        outputDictionary["LABEL RANKING AVERAGE PRECISION"] = label_ranking_average_precision_score(y_true=y_test,y_score=y_score)
    except:
        outputDictionary["LABEL RANKING AVERAGE PRECISION"] = str(np.nan)
    try:
        outputDictionary["COVARAGE"] = coverage_error(y_true=y_test,y_score=y_score)
    except:
        outputDictionary["COVARAGE"] = str(np.nan)



    try:
        outputDictionary["AUCROC MICRO"] = roc_auc_score(y_true=y_test,y_score=y_score, average="micro")
    except:
        outputDictionary["AUCROC MICRO"] = str(np.nan)

    try:
        outputDictionary["AUCROC MACRO"] = roc_auc_score(y_true=y_test,y_score=y_score, average="macro")
    except:
        outputDictionary["AUCROC MACRO"] = str(np.nan)

    try:
        outputDictionary["AUCROC SAMPLES"] = roc_auc_score(y_true=y_test,y_score=y_score, average="samples")
    except:
        outputDictionary["AUCROC SAMPLES"] = str(np.nan)

    try:
        outputDictionary["AUCROC WEIGHTED"] = roc_auc_score(y_true=y_test,y_score=y_score, average="weighted")
    except:
        outputDictionary["AUCROC WEIGHTED"] = str(np.nan)



    try:
        outputDictionary["HAMMING LOSS example based"] = hamming_loss(y_true=y_test, y_pred=pred)
    except:
        outputDictionary["HAMMING LOSS example based"] = str(np.nan)
    try:
        outputDictionary["PRECISION example based"] = precision_score(y_true=y_test, y_pred=pred, average="samples")
    except:
        outputDictionary["PRECISION example based"] = str(np.nan)
    try:
        outputDictionary["RECALL example based"] = recall_score(y_true=y_test, y_pred=pred, average="samples")
    except:
        outputDictionary["RECALL example based"] = str(np.nan)
    try:
        outputDictionary["F1 example based"] = f1_score(y_true=y_test, y_pred=pred, average="samples")
    except:
        outputDictionary["F1 example based"] = str(np.nan)
    try:
        outputDictionary["ACCURACY example-based"] = jaccard_similarity_score(y_true=y_test, y_pred=pred)
    except:
        outputDictionary["ACCURACY example-based"] = str(np.nan)
    try:
        outputDictionary["SUBSET ACCURACY"] = accuracy_score(y_true=y_test, y_pred=pred)
    except:
        outputDictionary["SUBSET ACCURACY"] = str(np.nan)

    try:
        outputDictionary["MACRO PRECISION"] = precision_score(y_true=y_test, y_pred=pred, average="macro")
    except:
        outputDictionary["MACRO PRECISION"] = str(np.nan)
    try:
        outputDictionary["MICRO PRECISION"] = precision_score(y_true=y_test, y_pred=pred, average="micro")
    except:
        outputDictionary["MICRO PRECISION"] = str(np.nan)
    try:
        outputDictionary["WEIGHTED PRECISION"] = precision_score(y_true=y_test, y_pred=pred, average="weighted")
    except:
        outputDictionary["WEIGHTED PRECISION"] = str(np.nan)

    try:
        outputDictionary["MACRO RECALL"] = recall_score(y_true=y_test, y_pred=pred, average="macro")
    except:
        outputDictionary["MACRO RECALL"] = str(np.nan)
    try:
        outputDictionary["MICRO RECALL"] = recall_score(y_true=y_test, y_pred=pred, average="micro")
    except:
        outputDictionary["MICRO RECALL"] = str(np.nan)
    try:
        outputDictionary["WEIGHTED RECALL"] = recall_score(y_true=y_test, y_pred=pred, average="weighted")
    except:
        outputDictionary["WEIGHTED RECALL"] = str(np.nan)


    try:
        outputDictionary["MACRO F1"] = f1_score(y_true=y_test, y_pred=pred, average="macro")
    except:
        outputDictionary["MACRO F1"] = str(np.nan)
    try:
        outputDictionary["MICRO F1"] = f1_score(y_true=y_test, y_pred=pred, average="micro")
    except:
        outputDictionary["MICRO F1"] = str(np.nan)
    try:
        outputDictionary["WEIGHTED F1"] = f1_score(y_true=y_test, y_pred=pred, average="weighted")
    except:
        outputDictionary["WEIGHTED F1"] = str(np.nan)

    try:
        outputDictionary["ZERO ONE LOSS"] = zero_one_loss(y_true=y_test, y_pred=pred)
    except:
        outputDictionary["ZERO ONE LOSS"] = str(np.nan)


    try:
        outputDictionary["AUPRC MACRO"] = average_precision_score(y_true=y_test, y_score=y_score, average="macro")
    except:
        outputDictionary["AUPRC MACRO"] = str(np.nan)
    try:
        outputDictionary["AUPRC MICRO"] = average_precision_score(y_true=y_test, y_score=y_score, average="micro")
    except:
        outputDictionary["AUPRC MICRO"] = str(np.nan)
    try:
        outputDictionary["AUPRC SAMPLE"] = average_precision_score(y_true=y_test, y_score=y_score, average="samples")
    except:
        outputDictionary["AUPRC SAMPLE"] = str(np.nan)
    try:
        outputDictionary["AUPRC WEIGHTED"] = average_precision_score(y_true=y_test, y_score=y_score, average="weighted")
    except:
        outputDictionary["AUPRC WEIGHTED"] = str(np.nan)


    outputDictionary["timeForEval"] = timeForEval

    try:
        outputDictionary["Classification report"] = classification_report(y_true=y_test, y_pred=y_score)
    except:
        outputDictionary["Classification report"] = str(np.nan)

    try:
        outputDictionary["ONE ERROR"] = one_error(y_true=y_test, y_score=y_score)
    except:
        outputDictionary["ONE ERROR"] = one_error(y_true=y_test, y_score=y_score)


    #print("Statistics from MEKA: ", clf._statistics)
    d["model_name_ts"] = filename
    d["dataSet_name"] = dataSetName
    d["numberEvaluatedModels"] = x + 1
    d["NumberOfRemoveValuesWhenEvaluating"] = removedValues
    d["system_config"] = {"CPU":platform.processor(), "uname":list(platform.uname()), "RAM":'20GB', "node": platform.node(), "python_version":platform.python_version(), "python_compiler":platform.python_compiler(), "platform": platform.platform()}
    d["measures"] = outputDictionary

    #try:
    #    os.mkdir(methodName)
    #except:
    #    pass

    print(d)

    with open(filename + ".json", "w") as outFile:
            json.dump(d, outFile)

    print("Successfull Evaluation")
