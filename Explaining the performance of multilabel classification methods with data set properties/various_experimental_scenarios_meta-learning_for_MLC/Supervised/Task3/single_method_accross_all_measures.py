import pandas as pd
import numpy as np
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


metriccccc = ['ACCURACY_example_based', 'AUCROC_MICRO', 'AUPRC_MICRO',
              'COVARAGE', 'F1_example_based', 'HAMMING_LOSS_example_based',
              'LABEL_RANKING_AVERAGE_PRECISION', 'LABEL_RANKING_LOSS',
              'MACRO_F1', 'MACRO_PRECISION', 'MACRO_RECALL', 'MICRO_F1',
              'MICRO_PRECISION', 'MICRO_RECALL', 'ONE_ERROR',
              'PRECISION_example_based', 'RECALL_example_based',
              'SUBSET_ACCURACY']

vvvv = defaultdict(dict)
cnt = 0
forDataSet = []

for node in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
    res_all_nodes = defaultdict(dict)
    #for metric in metriccccc:
    vvv = []
    zz = []
    qq = []
    datasetNamesTOStore = []

    pomList = []
    x = 0
    selectedDatasets = []
    numDatasetsTest = 40

    metrics_test = defaultdict(dict)

    print("Processing node {}".format(node))
    while x < numDatasetsTest:
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
                   'ECCJ48', 'TREMLCnew', 'MBR', 'RFPCT', "EBRJ48", 'RSMLCC', "SSM", "CDN"]


            data = data.drop(targets, axis=1)
            dataset_name_test = datasets.pop(integ)
            selectedDatasets.append(dataset_name_test)
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

                lc =  LeaveOneOut()
                errors_validation = {}
                ls = []
                predictions = defaultdict(dict)

                for X_train_index, X_test_index in lc.split(X, y):
                    X_train = X[X_train_index,:]
                    y_train = y[X_train_index]
                    X_test = X[X_test_index, :]
                    y_test = y[X_test_index]
                    pomDict = {}
                    #rf = RandomForestRegressor(n_estimators=5, max_features=int(na_free.shape[1]/3), max_depth=None)
                    rf = DecisionTreeRegressor(min_samples_split=node, max_depth=None, random_state=42)
                    #rf = KNeighborsRegressor(5)
                    rf.fit(X_train, y_train)
                    prediction = rf.predict(X_test)
                    errors_validation[na_free.iloc[X_test_index, 0].values[0]] = mean_absolute_error(y_test, prediction)
                    ls.append(mean_absolute_error(y_test, prediction))

                    pomDict["true"] = y_test[0]
                    pomDict["prediction"] = prediction[0]
                    predictions[na_free.iloc[X_test_index, 0].values[0]] = pomDict


                metrics[key] = pd.DataFrame(errors_validation, index=[0]).mean().values[0]
                rf.fit(X, y)
                regressors[key] = rf


            finalFrame = defaultdict(dict)

            for key in list(only_na.groupby(["metric"]).groups):
                X = only_na.iloc[doGroup_test[key], 1:-2].values
                y = only_na.iloc[doGroup_test[key], -2].values
                dd = {}
                pred = regressors[key].predict(X)
                dd["true_values"] = y
                dd["predict_values"] = pred
                dd["MAE"] = mean_absolute_error(y_true=y, y_pred=pred)
                dd["validation_error_all_39_datasets"] = metrics[key]
                dd["metrics_name"] = key
                dd["number_nodes"] = node
                finalFrame[key] = dd
                name_metric = key
                forDataSet.append(pd.DataFrame(finalFrame[name_metric], index=[dataset_name_test]))


    # kk = []
    # for x in list(forDataSet.keys()):
    #     kk.append(forDataSet[x])
    # final = pd.concat(kk, axis=0)
    # q = []
    # for x in range(0, 40):
    #     q.append(np.abs(final.true_values[x] - final.predict_values[x]))
    #
    # plt.scatter(final.iloc[:, 0], q)
    # for x in range(0, 40):
    #     plt.text(final.iloc[x, 0], q[x], final.index[x])
    # z = []
    # for x in range(0, 40):
    #     z.append(np.abs(final.true_values[x] - final.true_values.mean()))
    #
    # print("Baseline mean: ", np.mean(z))
    # print("Baseline std: ", np.std(z))
    #
    # print("ABs mean error: ", np.mean(q))
    # print("ABs std error: ", np.std(q))
    #
    # qqqqq = {}
    # qqqqq["MAE_STD"] =  np.mean(z)
    # qqqqq["MAE_STD"] =  np.std(z)
    # qqqqq["mean_abs"] =  np.mean(q)
    # qqqqq["std_abs"] =  np.std(q)
    # res_all_nodes[node] = qqqqq
    # cnt +=1
    # if cnt == 2:
    #     break
    # break



large_data_frame = pd.concat(forDataSet, axis=0)
large_data_frame = large_data_frame.reset_index()

group_results_by_metric = large_data_frame.groupby(["metrics_name", "number_nodes"]).groups



list_nodes = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

d = {}


metriccccc = ['ACCURACY_example_based', 'AUCROC_MICRO', 'AUPRC_MICRO',
              'F1_example_based', 'HAMMING_LOSS_example_based',
              'MACRO_F1', 'MACRO_PRECISION', 'MACRO_RECALL', 'MICRO_F1',
              'MICRO_PRECISION', 'MICRO_RECALL', 'PRECISION_example_based', 'RECALL_example_based',
              'SUBSET_ACCURACY']


for idx, met in enumerate(metriccccc):
    choose_list = []
    for node in list_nodes:
        choose_list.append(large_data_frame.iloc[group_results_by_metric[met, node]].mean().loc["validation_error_all_39_datasets"])

    d[met] = list_nodes[np.argmin(choose_list)]
    # plt.figure(idx)
    # plt.scatter(list_nodes, choose_list)
    # plt.title(met)


ff = {}
for key in d.keys():
    print("{} is {} +/ {}".format(key, large_data_frame.iloc[group_results_by_metric[key, d[key]]].mean().loc["MAE"], large_data_frame.iloc[group_results_by_metric[key, d[key]]].std().loc["MAE"]))
    s = {}
    s["mean"] = large_data_frame.iloc[group_results_by_metric[key, d[key]]].mean().loc["MAE"]
    s["std"] = large_data_frame.iloc[group_results_by_metric[key, d[key]]].std().loc["MAE"]
    s["baseline_mean"] = np.abs(large_data_frame.iloc[group_results_by_metric[key, d[key]]].loc[:, "true_values"] - large_data_frame.iloc[group_results_by_metric[key, d[key]]].loc[:, "true_values"].mean()).mean()
    s["baseline_std"] = np.abs(large_data_frame.iloc[group_results_by_metric[key, d[key]]].loc[:, "true_values"] - large_data_frame.iloc[group_results_by_metric[key, d[key]]].loc[:, "true_values"].mean()).std()
    ff[key] = s

print(pd.DataFrame(ff).T)

pd.DataFrame(ff).T.round(3).to_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task3/Results/Ada300_res.csv")


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