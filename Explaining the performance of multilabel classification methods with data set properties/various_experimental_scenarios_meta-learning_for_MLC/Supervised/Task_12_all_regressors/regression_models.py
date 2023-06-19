import os
import pickle
import pandas as pd
import numpy as np
import matplotlib
import copy

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


from sklearn.metrics import mean_absolute_error



from random import randint


metriccccc = ['ACCURACY_example_based', 'AUCROC_MICRO', 'AUPRC_MICRO',
              'COVARAGE', 'F1_example_based', 'HAMMING_LOSS_example_based',
              'LABEL_RANKING_AVERAGE_PRECISION', 'LABEL_RANKING_LOSS',
              'MACRO_F1', 'MACRO_PRECISION', 'MACRO_RECALL', 'MICRO_F1',
              'MICRO_PRECISION', 'MICRO_RECALL', 'ONE_ERROR',
              'PRECISION_example_based', 'RECALL_example_based',
              'SUBSET_ACCURACY']
# methods = ['MLkNN', 'MLARM', 'DEEP1',
#            'PCT', 'BPNN', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
#            'BR', 'HOMER', 'RFDTBR', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
#            'EBRJ48', 'TREMLCnew', 'MBR', 'ECCJ48', "Ada300", 'RSMLCC', "SSM", "CDN", "RFPCT"]

methods = ['MLkNN', 'MLARM', 'DEEP1',
       'PCT', 'BPNN', 'RFPCT', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
       'BR', 'HOMER', 'Ada300', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
       'RFDTBR', 'TREMLCnew', 'MBR', 'CDN', 'ECCJ48', 'EBRJ48', 'SSM',
       'RSMLCC']

targets = ['MLkNN', 'MLARM', 'DEEP1',
           'PCT', 'BPNN', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
           'BR', 'HOMER', 'RFDTBR', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
           'EBRJ48', 'TREMLCnew', 'MBR', 'ECCJ48', "Ada300", 'RSMLCC', "SSM", "CDN", "RFPCT"]

datasets = ['medical',
 'birds',
 'proteins_plant',
 'emotions',
 'enron',
 'foodtruck',
 'delicious',
 'scene',
 'HumanPseAAC',
 'ABPM',
 'corel5k',
 'yeast',
 'HumanGO',
 'GpositivePseAAC',
 'cal500',
 'stackex_cs',
 'ohsumed',
 'Virus_PseAAC',
 'ng20',
 'Arabic200',
 'genbase',
 'stackex_chess',
 'GpositiveGO',
 'PlantGO',
 'GnegativeGO',
 'bibtex',
 'slashdot',
 'tmc2007_500',
 'langlog',
 'stackex_philosophy',
 'reutersk500',
 'proteins_human',
 'Water_quality',
 'PlantPseAAC',
 'Yelp',
 'CHD_49',
 'flags',
 'proteins_virus',
 'VirusGO',
 'GnegativePseACC']


def calculate_test_error(for_every_method, metrics, datasets):
    method_err = defaultdict(dict)
    for method in for_every_method.keys():
        me_err = defaultdict(dict)
        for metric in metrics:
            metric_err = defaultdict(list)
            for dataset in datasets:
                metric_err["val_err_mean"].append(for_every_method[method][dataset][metric]["validation_error_mean"])
                # d["val_err_std"] = for_every_method[method][dataset]["MACRO_F1"]["validation_error_std"]
                metric_err["test_err_mean"].append(for_every_method[method][dataset][metric]["test_error"])
            me_err[metric] = metric_err
        method_err[method] = me_err
    return method_err


def plot_fcn(results_to_plot):
    for method in list(results_to_plot.keys()):
        for metric in list(results_to_plot[method].keys()):

            plt.scatter(np.arange(len(results_to_plot[method][metric]["test_err_mean"])),
                        results_to_plot[method][metric]["test_err_mean"], c="red",
                        label=str(np.mean(results_to_plot[method][metric]["test_err_mean"])))
            plt.scatter(np.arange(len(results_to_plot[method][metric]["test_err_mean"])),
                        results_to_plot[method][metric]["val_err_mean"],
                        c="green", label=str(np.mean(results_to_plot[method][metric]["val_err_mean"])))
            plt.xticks(np.arange(len(results_to_plot[method][metric]["test_err_mean"])), datasets, rotation=90)
            plt.legend()
            try:
                os.mkdir(
                    "/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_12_all_regressors/datasets/" + method)
            except:
                print(" ")
            plt.savefig(
                "/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_12_all_regressors/datasets/" + method + "/" + method + "_" + metric + "_" + str(
                    number_trees) + ".svg")

            try:
                os.mkdir(
                    "/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_12_all_regressors/results/" + method)
            except:
                print(" ")
            with open(
                    "/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_12_all_regressors/results/" + method + "/" + method + "_" + metric + "_" + str(
                            number_trees) + "_.pickle", "wb") as file:
                pickle.dump(obj=results_to_plot[method][metric], file=file)
            plt.close()


# for number_trees in [8, 10, 16, 20]:
for number_trees in [8]:
    for_every_method = defaultdict(dict)
    for method in methods[:2]:
        for_every_dataset = defaultdict(list)
        pomList = []
        x = 0
        selectedDatasets = []
        numDatasetsTest = 40
        method_store_regressor = defaultdict(dict)

        while x<numDatasetsTest:
            integ = randint(0, 39)
            if integ in pomList:
                continue
            else:
                data = pd.read_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_12_all_regressors/NotScaled_meta_features.csv")
                data = data.iloc[:, 1:]
                datasets = data.iloc[:40, 0].tolist()
                targets.remove(method)
                data = data.drop(targets, axis=1)
                dataset_name_test = datasets.pop(integ)
                selectedDatasets.append(dataset_name_test)
                pomList.append(integ)
                print("ID: {}, DATASET: {}".format(x+1, dataset_name_test))
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
                dataset_results = {}

                for key in list(na_free.groupby(["metric"]).groups):
                    X = na_free.iloc[doGroup_train[key], 1:-2].values
                    # print(X.shape)
                    y = na_free.iloc[doGroup_train[key], -2].values
                    lc =  LeaveOneOut()
                    errors = {}
                    ls = []
                    predictions = defaultdict(dict)
                    err_ = []

                    for X_train_index, X_test_index in lc.split(X, y):
                        X_train = X[X_train_index,:]
                        y_train = y[X_train_index]
                        X_test = X[X_test_index, :]
                        y_test = y[X_test_index]
                        pomDict = {}
                        #rf = RandomForestRegressor(n_estimators=5, max_features=int(na_free.shape[1]/3), max_depth=None)
                        rf = DecisionTreeRegressor(min_samples_split=number_trees, max_depth=None, random_state=42)
                        #rf = KNeighborsRegressor(5)
                        rf.fit(X_train, y_train)
                        prediction = rf.predict(X_test)
                        errors[na_free.iloc[X_test_index, 0].values[0]] = mean_absolute_error(y_test, prediction)
                        pomDict["true"] = y_test[0]
                        pomDict["prediction"] = prediction[0]
                        predictions[na_free.iloc[X_test_index, 0].values[0]] = pomDict
                        err_.append(mean_absolute_error(y_test, prediction))

                    metrics[key] = predictions
                    rf.fit(X, y)
                    # print(X.shape)
                    regressors[key] = rf
                    # print("metric: {}, dataset name: {} prediction: {}".format(key, dataset_name_test, np.abs(only_na.iloc[doGroup_test[key], -2].values[0] - rf.predict(only_na.iloc[doGroup_test[key], 1:-2])[0])))
                    dataset_results[key] = {"true": only_na.iloc[doGroup_test[key], -2].values[0],
                                            "predicted":rf.predict(only_na.iloc[doGroup_test[key], 1:-2])[0],
                                            "validation":predictions,
                                            "validation_error_mean":np.mean(err_),
                                            "validation_error_std": np.std(err_),
                                            "test_error": np.abs(only_na.iloc[doGroup_test[key], -2].values[0] - rf.predict(only_na.iloc[doGroup_test[key], 1:-2])[0])}
                for_every_dataset[dataset_name_test] = dataset_results
                x += 1
            targets = copy.copy(methods)

        for_every_method[method] = for_every_dataset

        regressors_to_store = {}
        data_pom = copy.copy(data.iloc[:, 1:])
        data_pom = data_pom.reset_index()
        data_pom = data_pom.drop(["index"], axis=1)
        pom_keys = data_pom.groupby(["metric"]).groups

        for key in list(pom_keys):
            X = data_pom.iloc[pom_keys[key], :-2].values
            y = data_pom.iloc[pom_keys[key], -2].values
            print(data_pom.iloc[pom_keys[key], -2])
            regressors_to_store[key] = rf.fit(X, y)
            try:
                os.mkdir(
                    "/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_12_all_regressors/models/" + method)
            except:
                print(" ")
            with open("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_12_all_regressors/models/" + method + "/" + method + "_" + key + "_" + str(number_trees) + ".pickle", "wb") as file:
                pickle.dump(obj=regressors_to_store[key], file=file)
        method_store_regressor[method] = regressors_to_store


        results_to_plot = calculate_test_error(for_every_method, metriccccc, datasets)
        plot_fcn(results_to_plot)