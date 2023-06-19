import pandas as pd
import numpy as np

from collections import defaultdict

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import LeaveOneOut


from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


from random import randint

vvv = []
zz = []
qq = []
datasetNamesTOStore = []

pomList = []
x = 0
selectedDatasets = []
numDatasetsTest = 40
forDataSet = {}

while x<numDatasetsTest:
    integ = randint(0, 39)

    if integ in pomList:
        continue
    else:

        data = pd.read_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/metaDataset.csv")
        data = data.iloc[:, 1:]

        datasets = data.iloc[:40, 0].tolist()


        targets = ['MLkNN', 'MLARM', 'DEEP1',
               'PCT', 'BPNN', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
               'BR', 'HOMER', 'Ada300', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
               'RFDTBR', 'TREMLCnew', 'MBR', 'EBRJ48', "ECCJ48", 'RSMLCC', "SSM", "CDN"]


        data = data.drop(targets, axis=1)
        dataset_name_test = datasets.pop(integ)
        selectedDatasets.append(dataset_name_test)


        # while x<numDatasetsTest :
        #     integ = randint(0, 39)
        #
        #     if integ in pomList:
        #         continue
        #     else:
        #         print(integ)
        #         dataset_name_test = datasets.pop(integ)
        #         datasets = data.iloc[:40, 0].tolist()
        #         selectedDatasets.append(dataset_name_test)
        pomList.append(integ)
        x += 1

        data.index = data.iloc[:, 0]
        na_free = data.drop(selectedDatasets, axis=0)
        selectedDatasets = []
        only_na = data[~data.index.isin(na_free.index)]

        na_free = na_free.drop(["index"], axis=1)
        na_free = na_free.reset_index()

        only_na = only_na.drop(["index"], axis=1)
        only_na = only_na.reset_index()


        doGroup_train = na_free.groupby(["metric"]).groups
        doGroup_test = only_na.groupby(["metric"]).groups

        metrics = defaultdict(dict)

        regressors = {}

        for key in list(na_free.groupby(["metric"]).groups):

            X = na_free.iloc[doGroup_train[key], 1:-2].values
            y = na_free.iloc[doGroup_train[key], -2].values


            #rf = DecisionTreeRegressor(min_samples_split=8)
            lc =  LeaveOneOut()

            errors = {}
            ls = []

            predictions = defaultdict(dict)

            for X_train_index, X_test_index in lc.split(X, y):
                X_train = X[X_train_index,:]
                y_train = y[X_train_index]
                X_test = X[X_test_index, :]
                y_test = y[X_test_index]
                pomDict = {}
                #rf = RandomForestRegressor(n_estimators=5, max_features=int(na_free.shape[1]/3), max_depth=None)
                #rf = DecisionTreeRegressor(min_samples_split=10, max_depth=None)
                rf = KNeighborsRegressor(6)
                rf.fit(X_train, y_train)
                prediction = rf.predict(X_test)
                errors[na_free.iloc[X_test_index, 0].values[0]] = mean_absolute_error(y_test, prediction)
                ls.append(mean_absolute_error(y_test, prediction))

                pomDict["true"] = y_test[0]
                pomDict["prediction"] = prediction[0]
                predictions[na_free.iloc[X_test_index, 0].values[0]] = pomDict


            metrics[key] = predictions

            rf.fit(X, y)
            regressors[key] = rf


        ########################## Sub-learning problem 2
        targetsForMetric = defaultdict(dict)

        pp = {}
        for key in list(doGroup_train.keys()):
            pom = pd.DataFrame(metrics[key]).T
            pp[key] =  np.mean(np.abs(pom.iloc[:, 0] - pom.iloc[:, 1]))
            targetsForMetric[key] = np.where(np.abs(pom.iloc[:, 0] - pom.iloc[:, 1]) > pp[key], 1, 0)

            #print("For measure {} the absolute error is {} with std {}".format(key, np.mean(np.abs(pom.iloc[:, 0] - pom.iloc[:, 1])), np.std(np.abs(pom.iloc[:, 0] - pom.iloc[:, 1]))))




        results = defaultdict(dict)
        classifiers = {}
        for key in list(doGroup_train.keys()):
            X = na_free.iloc[doGroup_train[key], 1:-2].values
            y = targetsForMetric[key]

            #rf = DecisionTreeRegressor(min_samples_split=8)
            lc =  LeaveOneOut()

            errors_clf = {}
            ls_clf = []

            predictions = defaultdict(dict)

            for X_train_index, X_test_index in lc.split(X, y):
                X_train = X[X_train_index,:]
                y_train = y[X_train_index]
                X_test = X[X_test_index, :]
                y_test = y[X_test_index]
                pomDict = {}
                #rf_clf = RandomForestClassifier(n_estimators=5, min_samples_split=6 ,max_depth=None, max_features=int(na_free.shape[1]/2), class_weight="balanced")
                #rf_clf = DecisionTreeClassifier(min_samples_split=8, max_depth=None, min_samples_leaf=4)
                #rf_clf = DecisionTreeClassifier(min_samples_split=6, max_depth=None, min_samples_leaf=4)
                rf_clf = KNeighborsClassifier(5)
                #rf_clf = LogisticRegression(solver="lbfgs", max_iter=400)
                rf_clf.fit(X_train, y_train)
                prediction = rf_clf.predict(X_test)
                #errors_clf[na_free.iloc[X_test_index, 0].values[0]] = f1_score(y_test, prediction)
                #ls_clf.append(f1_score(y_test, prediction))

                pomDict["true"] = y_test[0]
                pomDict["prediction"] = prediction[0]
                predictions[na_free.iloc[X_test_index, 0].values[0]] = pomDict

            results[key] = predictions
            rf_clf.fit(X, y)
            classifiers[key] = rf_clf

        finalFrame = defaultdict(dict)

        for key in list(only_na.groupby(["metric"]).groups):
            X = only_na.iloc[doGroup_test[key], 1:-2].values
            y = only_na.iloc[doGroup_test[key], -2].values

            dd = {}
            #for i in range(na_free.shape[0]):
            pred = regressors[key].predict(X)
            dd["true_values"] = y
            dd["predict_values"] = pred
            dd["meta_true"] = np.where(np.abs(pred-y) > pp[key], 1, 0)
            dd["meta_predicted"] = classifiers[key].predict(X)
            finalFrame[key] = dd
            #forDataSet[dataset_name_test] = dd

        zz.append(pd.DataFrame(finalFrame["AUCROC_MICRO"]))
        vvv.append(pd.DataFrame(finalFrame))
        datasetNamesTOStore.append(dataset_name_test)
        print("###################")
        print("For dataset {}".format(dataset_name_test))
        print("###################")
        print(pd.DataFrame(finalFrame["AUCROC_MICRO"]))
        pom = pd.DataFrame(metrics["AUCROC_MICRO"])
        print(mean_absolute_error(pom.iloc[:, 0], pom.iloc[:, 1]))
        qq.append(pp["AUCROC_MICRO"])
        forDataSet[dataset_name_test] = pd.DataFrame(finalFrame["AUCROC_MICRO"])
        #v = pd.DataFrame(na_free.columns[1:-2]).loc[np.where(rf.feature_importances_ > 0.05, True, False)] # There are 4 important properties. SCUMBLE, ration of number of instnaces to number of attributes diversity and label cardinality WITH 100 TREES

x = pd.concat(zz)
print(accuracy_score(x.iloc[:, 2], x.iloc[:, 3]))

z = pd.DataFrame(results["AUCROC_MICRO"]).T
print(accuracy_score(z.iloc[:, 0], z.iloc[:, 1]))


pom = []
for dataset_name, dataset_results in enumerate(vvv):
    res = dataset_results.T
    res.true_values = res.true_values.apply(lambda x: x[0])
    res.predict_values = res.predict_values.apply(lambda x: x[0])
    res.meta_true = res.meta_true.apply(lambda x: x[0])
    res.meta_predicted = res.meta_predicted.apply(lambda x: x[0])
    pom.append(res)

ff = pd.concat(pom)
ff = ff.reset_index()
groupsRes = ff.groupby(by=["index"]).groups


for key in list(groupsRes.keys()):
    pomFrame = ff.iloc[groupsRes[key], 1:]
    print("#################################")
    print("For the measure {} the MAE is {} with std {}".format(key,
                                                                np.mean(np.abs(pomFrame.true_values-pomFrame.predict_values)),
                                                                np.std(np.abs(pomFrame.true_values-pomFrame.predict_values))))
    print("For the measure {} the classification acc is {}, f1 is {}, precision is {}, recall is {}".format(key, accuracy_score(pomFrame.meta_true, pomFrame.meta_predicted),
                                                                                                            f1_score(pomFrame.meta_true, pomFrame.meta_predicted),
                                                                                                            precision_score(pomFrame.meta_true, pomFrame.meta_predicted),
                                                                                                            recall_score(pomFrame.meta_true, pomFrame.meta_predicted)))
    print("#################################")