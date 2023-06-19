import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import shap
import matplotlib.pyplot as plt

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

metriccccc = ['ACCURACY_example_based', 'AUCROC_MICRO', 'AUPRC_MICRO',
              'COVARAGE', 'F1_example_based', 'HAMMING_LOSS_example_based',
              'LABEL_RANKING_AVERAGE_PRECISION', 'LABEL_RANKING_LOSS',
              'MACRO_F1', 'MACRO_PRECISION', 'MACRO_RECALL', 'MICRO_F1',
              'MICRO_PRECISION', 'MICRO_RECALL', 'ONE_ERROR',
              'PRECISION_example_based', 'RECALL_example_based',
              'SUBSET_ACCURACY']

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
               'BR', 'HOMER', 'RFDTBR', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
               'EBRJ48', 'TREMLCnew', 'MBR', 'ECCJ48', "Ada300", 'RSMLCC', "SSM", "CDN"]


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
                rf = DecisionTreeRegressor(min_samples_split=10, max_depth=None, random_state=42)
                #rf = KNeighborsRegressor(5)
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
        # targetsForMetric = defaultdict(dict)
        #
        # pp = {}
        # for key in list(doGroup_train.keys()):
        #     pom = pd.DataFrame(metrics[key]).T
        #     pp[key] =  np.mean(np.abs(pom.iloc[:, 0] - pom.iloc[:, 1]))
        #     targetsForMetric[key] = np.where(np.abs(pom.iloc[:, 0] - pom.iloc[:, 1]) > pp[key], 1, 0)

            #print("For measure {} the absolute error is {} with std {}".format(key, np.mean(np.abs(pom.iloc[:, 0] - pom.iloc[:, 1])), np.std(np.abs(pom.iloc[:, 0] - pom.iloc[:, 1]))))




        results = defaultdict(dict)
        classifiers = {}
        # for key in list(doGroup_train.keys()):
        #     X = na_free.iloc[doGroup_train[key], 1:-2].values
        #     y = targetsForMetric[key]
        #
        #     #rf = DecisionTreeRegressor(min_samples_split=8)
        #     lc =  LeaveOneOut()
        #
        #     errors_clf = {}
        #     ls_clf = []
        #
        #     predictions = defaultdict(dict)
        #
        #     for X_train_index, X_test_index in lc.split(X, y):
        #         X_train = X[X_train_index,:]
        #         y_train = y[X_train_index]
        #         X_test = X[X_test_index, :]
        #         y_test = y[X_test_index]
        #         pomDict = {}
        #         #rf_clf = RandomForestClassifier(n_estimators=5, min_samples_split=6 ,max_depth=None, max_features=int(na_free.shape[1]/2), class_weight="balanced")
        #         #rf_clf = DecisionTreeClassifier(min_samples_split=10, max_depth=None, min_samples_leaf=2)
        #         #rf_clf = DecisionTreeClassifier(min_samples_split=6, max_depth=None, min_samples_leaf=4)
        #         rf_clf = KNeighborsClassifier(5)
        #         #rf_clf = LogisticRegression(solver="lbfgs", max_iter=400)
        #         rf_clf.fit(X_train, y_train)
        #         prediction = rf_clf.predict(X_test)
        #         #errors_clf[na_free.iloc[X_test_index, 0].values[0]] = f1_score(y_test, prediction)
        #         #ls_clf.append(f1_score(y_test, prediction))
        #
        #         pomDict["true"] = y_test[0]
        #         pomDict["prediction"] = prediction[0]
        #         predictions[na_free.iloc[X_test_index, 0].values[0]] = pomDict
        #
        #     results[key] = predictions
        #     rf_clf.fit(X, y)
        #     classifiers[key] = rf_clf

        finalFrame = defaultdict(dict)

        for key in list(only_na.groupby(["metric"]).groups):
            X = only_na.iloc[doGroup_test[key], 1:-2].values
            y = only_na.iloc[doGroup_test[key], -2].values

            dd = {}
            #for i in range(na_free.shape[0]):
            pred = regressors[key].predict(X)
            dd["true_values"] = y
            dd["predict_values"] = pred
            #dd["meta_true"] = np.where(np.abs(pred-y) > pp[key], 1, 0)
            #dd["meta_predicted"] = classifiers[key].predict(X)
            finalFrame[key] = dd
            #forDataSet[dataset_name_test] = dd




        name_metric = metriccccc[1]

        zz.append(pd.DataFrame(finalFrame[name_metric]))
        vvv.append(pd.DataFrame(finalFrame))
        datasetNamesTOStore.append(dataset_name_test)
        print("###################")
        print("For dataset {}".format(dataset_name_test))
        print("###################")
        print(pd.DataFrame(finalFrame[name_metric]))
        pom = pd.DataFrame(metrics[name_metric])
        #print(mean_absolute_error(pom.iloc[:, 0], pom.iloc[:, 1]))
        #qq.append(pp["AUCROC_MICRO"])
        forDataSet[dataset_name_test] = pd.DataFrame(finalFrame[name_metric], index=[dataset_name_test])
        #v = pd.DataFrame(na_free.columns[1:-2]).loc[np.where(rf.feature_importances_ > 0.05, True, False)] # There are 4 important properties. SCUMBLE, ration of number of instnaces to number of attributes diversity and label cardinality WITH 100 TREES

#x = pd.concat(zz)
#print(accuracy_score(x.iloc[:, 2], x.iloc[:, 3]))
#
# z = pd.DataFrame(results["AUCROC_MICRO"]).T
# print(accuracy_score(z.iloc[:, 0], z.iloc[:, 1]))
#
#
# pom = []
# for dataset_name, dataset_results in enumerate(vvv):
#     res = dataset_results.T
#     res.true_values = res.true_values.apply(lambda x: x[0])
#     res.predict_values = res.predict_values.apply(lambda x: x[0])
#  #  res.meta_true = res.meta_true.apply(lambda x: x[0])
#  #   res.meta_predicted = res.meta_predicted.apply(lambda x: x[0])
#     pom.append(res)
#
# ff = pd.concat(pom)
# ff = ff.reset_index()
# groupsRes = ff.groupby(by=["index"]).groups

kk = []
for x in list(forDataSet.keys()):
    kk.append(forDataSet[x])

final = pd.concat(kk, axis=0)

q = []
for x in range(0, 40):
    q.append(np.abs(final.iloc[x, 0] - final.iloc[x, 1]))

plt.scatter(final.iloc[:, 0], q)
for x in range(0, 40):
    plt.text(final.iloc[x, 0], q[x], final.index[x])

#plt.savefig("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task1/store_images_EBRJ48/true_vs_error" + name_metric + ".pdf", bbox_inches="tight")

#plt.close()

tt = np.where(np.array(q) > 0.2, 0, 1)
tt1 = np.where(np.array(q) > 0.2, True, False)

z = []
for x in range(0, 40):
    z.append(np.abs(final.iloc[x, 0] - final.iloc[:, 0].mean()))

print("Baseline mean: ",np.mean(z))
print("Baseline std: ",np.std(z))

print("ABs mean error: ", np.mean(q))
print("ABs std error: ", np.std(q))
print(np.multiply(tt, np.array(q)).mean())
print(np.multiply(tt, np.array(q)).std())
print(final[tt1])



from sklearn.decomposition import PCA
#from sklearn.manifold import TSNE
#pca = TSNE(2,random_state=42, perplexity=2)

#plt.figure(2)

#a = data[data.iloc[:, -1]==name_metric].iloc[:, 1:-2]
#components = pca.fit_transform(a)
#plt.scatter(components[:, 0], components[:, 1])
#for x in range(0, 40):
#    plt.text(components[x, 0], components[x, 1], data.iloc[x, 0])

#plt.savefig("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task1/store_images_RFPCT/TSNE_representation_data" + name_metric + ".pdf", bbox_inches="tight")

# for key in list(groupsRes.keys()):
#     pomFrame = ff.iloc[groupsRes[key], 1:]
#     print("#################################")
#     print("For the measure {} the MAE is {} with std {}".format(key,
#                                                                 np.mean(np.abs(pomFrame.true_values-pomFrame.predict_values)),
#                                                                 np.std(np.abs(pomFrame.true_values-pomFrame.predict_values))))
#  #   print("For the measure {} the classification acc is {}, f1 is {}, precision is {}, recall is {}".format(key, accuracy_score(pomFrame.meta_true, pomFrame.meta_predicted),
#   #                                                                                                          f1_score(pomFrame.meta_true, pomFrame.meta_predicted),
#   #                                                                                                          precision_score(pomFrame.meta_true, pomFrame.meta_predicted),
#   #                                                                                                          recall_score(pomFrame.meta_true, pomFrame.meta_predicted)))
#     print("#################################")
X = pd.DataFrame(X_test)
X.columns = data.columns[1:-2]

explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(pd.DataFrame(X))
shap.force_plot(explainer.expected_value, shap_values[0, :], matplotlib=True)
print("DATASET {}:".format(dataset_name_test))
print("true {} prediction {}".format(y_test, prediction))

# a = data.columns[1:-2]
# shap.summary_plot(shap_values, X, plot_type="violin", plot_size=0.4, max_display=51)