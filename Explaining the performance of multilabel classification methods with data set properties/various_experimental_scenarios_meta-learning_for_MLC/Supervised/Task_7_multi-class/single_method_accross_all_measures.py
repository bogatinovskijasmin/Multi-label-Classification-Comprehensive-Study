import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("tkagg")
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



targets = ['MLkNN', 'MLARM', 'DEEP1',
           'PCT', 'BPNN', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
           'BR', 'HOMER', 'RFDTBR', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
           'ECCJ48', 'TREMLCnew', 'MBR', 'RFPCT', "EBRJ48", 'RSMLCC', "SSM", "CDN", "Ada300"]

def generate_target_variable(data):
    valid_targets = data.columns[53:-1]
    valid_targets = ["RFPCT", "RFDTBR", "EBRJ48"]
    list_targets = []
    for x in range(data.shape[0]):
        if data.iloc[x, -1] not in ['COVARAGE', 'HAMMING_LOSS_example_based','LABEL_RANKING_LOSS','ONE_ERROR']:
            #print(np.argmax(data.loc[x, valid_targets].values, axis=0))
            list_targets.append(np.argmax(data.loc[x, valid_targets].values, axis=0))
            #print(valid_targets[np.argmax(data.loc[x, valid_targets].values)])
        else:
            list_targets.append(np.argmin(data.loc[x, valid_targets].values, axis=0))

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    encoded = le.fit_transform(np.array(list_targets))

    return pd.DataFrame(encoded, index=data.iloc[:, 1].tolist()), le

def generate_target_variable_AAPT(data):
    valid_targets = data.columns[53:-1]
    #valid_targets = ["RFPCT", "RFDTBR", "EBRJ48"]
    list_targets = []
    for x in range(data.shape[0]):
        if data.iloc[x, -1] not in ['COVARAGE', 'HAMMING_LOSS_example_based','LABEL_RANKING_LOSS','ONE_ERROR']:
            #print(np.argmax(data.loc[x, valid_targets].values, axis=0))
            list_targets.append(valid_targets[np.argmax(data.loc[x, valid_targets].values, axis=0)])
            #print(valid_targets[np.argmax(data.loc[x, valid_targets].values)])
        else:
            list_targets.append(valid_targets[np.argmin(data.loc[x, valid_targets].values, axis=0)])

    print(list_targets)
    binary_targets = []
    algorithm_adaptation = ['MLkNN', 'MLARM', 'DEEP1','PCT', 'BPNN', 'MLTSVM', 'DEEP4', 'CLEMS', 'RFPCT']

    for x in list_targets:
        if x in algorithm_adaptation:
            binary_targets.append(int(1))
        else:
            binary_targets.append(int(0))

    return pd.DataFrame(np.array(binary_targets), index=data.iloc[:, 1].tolist())


#for node in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]:
list_nodes = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

#list_nodes = [10]
for node in list_nodes:
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

            real_targets_labels = generate_target_variable_AAPT(data)
            real_targets_labels = real_targets_labels.reset_index()
            real_targets_labels.columns = ["dataset_name", "target"]
            real_targets_labels = real_targets_labels.reset_index()

            data = data.drop(["index", "Unnamed: 0"], axis=1)
            data = data.reset_index()
            to_help = data.loc[:, ["index", "metric"]]
            pd.merge(to_help, real_targets_labels, on=["index"]).to_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_9_AA_vs_PT/targets.csv")
            exit(-1)

            data = data.iloc[:, 1:]

            datasets = data.iloc[:40, 0].tolist()

            targets = ['MLkNN', 'MLARM', 'DEEP1',
                       'PCT', 'BPNN', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
                       'BR', 'HOMER', 'RFDTBR', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
                       'ECCJ48', 'TREMLCnew', 'MBR', 'RFPCT', "EBRJ48", 'RSMLCC', "SSM", "CDN", "Ada300"]


            data = data.drop(targets, axis=1)
            dataset_name_test = datasets.pop(integ)
            selectedDatasets.append(dataset_name_test)
            pomList.append(integ)
            x += 1
            data.index = data.iloc[:, 0]
            na_free = data.drop(selectedDatasets, axis=0)
            selectedDatasets = []
            only_na = data[~data.index.isin(na_free.index)]




            tgt_test = real_targets_labels[~data.index.isin(na_free.index)]
            tgt_test = tgt_test.reset_index()
            tgt_test = tgt_test.drop(["index"], axis=1)

            tgt_train = real_targets_labels[data.index.isin(na_free.index)]
            tgt_train = tgt_train.reset_index()
            tgt_train = tgt_train.drop(["index"], axis=1)


            na_free = na_free.drop(["index"], axis=1)
            na_free = na_free.reset_index()

            only_na = only_na.drop(["index"], axis=1)
            only_na = only_na.reset_index()
            doGroup_train = na_free.groupby(["metric"]).groups
            doGroup_test = only_na.groupby(["metric"]).groups

            metrics = defaultdict(dict)
            regressors = {}

            real_targets_labels = real_targets_labels.reset_index()
            real_targets_labels.drop(["index"], axis=1, inplace=True)

            for key in list(na_free.groupby(["metric"]).groups):

                X = na_free.iloc[doGroup_train[key], 1:-1].values
                y = tgt_train.iloc[doGroup_train[key]].values

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
                    rf = DecisionTreeClassifier(min_samples_split=node, max_depth=None, random_state=42)
                    #rf = KNeighborsRegressor(5)
                    rf.fit(X_train, y_train)
                    prediction = rf.predict(X_test)
                    errors_validation[na_free.iloc[X_test_index, 0].values[0]] = f1_score(y_test, prediction, labels=np.unique(real_targets_labels), average="macro")
                    ls.append(f1_score(y_test, prediction, labels=np.unique(real_targets_labels), average="macro"))

                    pomDict["true"] = y_test[0]
                    pomDict["prediction"] = prediction[0]
                    predictions[na_free.iloc[X_test_index, 0].values[0]] = pomDict


                metrics[key] = pd.DataFrame(errors_validation, index=[0]).mean().values[0]
                rf.fit(X, y)
                regressors[key] = rf


            finalFrame = defaultdict(dict)

            for key in list(only_na.groupby(["metric"]).groups):
                X = only_na.iloc[doGroup_test[key], 1:-1].values
                y = tgt_test.iloc[doGroup_test[key]].values
                dd = {}
                pred = regressors[key].predict(X)
                dd["true_values"] = y.reshape(-1)
                dd["predict_values"] = pred.reshape(-1)
                dd["MAE"] = f1_score(y, pred, labels=np.unique(real_targets_labels), average="micro")
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

    d[met] = list_nodes[np.argmax(choose_list)]
    plt.figure(idx)
    plt.scatter(list_nodes, choose_list)
    plt.title(met)


ff = {}
cnt = 100
for key in d.keys():
    print("{} is {} +/ {}".format(key, large_data_frame.iloc[group_results_by_metric[key, d[key]]].mean().loc["MAE"], large_data_frame.iloc[group_results_by_metric[key, d[key]]].std().loc["MAE"]))
    s = {}
    s["mean"] = large_data_frame.iloc[group_results_by_metric[key, d[key]]].mean().loc["MAE"]
    s["std"] = large_data_frame.iloc[group_results_by_metric[key, d[key]]].std().loc["MAE"]
    s["baselineMax_count"] = pd.value_counts(large_data_frame.iloc[group_results_by_metric[key, d[key]]].loc[:, "true_values"]).iloc[0]/ pd.value_counts(large_data_frame.iloc[group_results_by_metric[key, d[key]]].loc[:, "true_values"]).sum()


    meta_learner = DecisionTreeClassifier(min_samples_split=d[key], max_depth=None, random_state=42)
    meta_learner = meta_learner.fit(data.iloc[:40, 1:-1].values,  large_data_frame.iloc[group_results_by_metric[key, d[key]]].true_values)
    #data.iloc[group_results_by_metric[key, d[key]], 1:-1].values
    plt.figure(figsize=(16, 4))

    #ax.imshow(im, aspect='auto', extent=(20, 80, 20, 80), alpha=0.5)


    from sklearn.tree import plot_tree
    plt.figure(met)
    plot_tree(meta_learner, feature_names=data.columns[1:-1], filled=True, rounded=True)
    ax = plt.gca()
    plt.xlim(-2000, 2000)
    plt.ylim(-2000, 2000)
    #plt.savefig("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_7_multi-class/Results/images/multi_class_" + key + "_.svg", bbox="tight")
    #plt.show()
    cnt +=1


    ff[key] = s

print(pd.DataFrame(ff).T)

pd.DataFrame(ff).T.round(3).to_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_7_multi-class/Results/joint_results.csv")



# sktree.plot_tree(meta_learner, feature_names=meta_features.columns[1:], filled=True, rounded=True)
# ax = plt.gca()
# #plt.xlim(-100, 100)
# plt.savefig("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_7_multi-class/Results/AlgorithmAdaptation_vs_problemTrasnformation_DecisionTree" + measure + ".png")
# plt.show()




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