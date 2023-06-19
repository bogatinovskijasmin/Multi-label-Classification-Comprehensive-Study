import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sklearn.tree as sktree
from Meta_learning_MLC.LearningScenarios.reading_meta_features_creating_meta_targets import *

from sklearn.model_selection import LeaveOneOut
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

meta_dataset_path = "/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/DatasetsByEvaluationMetric/"
measure = "LABEL_RANKING_AVERAGE_PRECISION.csv"
riseOrDown = "rise"


def selecctFeatures(meta_features, target):
    nof_list = np.arange(1, 20)
    high_score = 0
    # Variable to store the optimum features
    nof = 0
    score_list = []
    for n in range(len(nof_list)):
        for train_index, test_index in loocv.split(meta_features):
            model = RandomForestClassifier(100, class_weight="balanced")
            rfe = RFE(model, nof_list[n])
            X_train_rfe = rfe.fit_transform(meta_features[train_index], target[train_index])
            X_test_rfe = rfe.transform(meta_features[test_index])
            model.fit(X_train_rfe, target[train_index])
            score = model.score(X_test_rfe, target[test_index])
            score_list.append(score)

            if (score > high_score):
                high_score = score
                nof = nof_list[n]

    print("Optimum number of features: %d" % nof)
    print("Score with %d features: %f" % (nof, high_score))
    return nof


meta_features, meta_tar = read_meta_dataset_for_measure(meta_dataset_path, measure)

#meta_features = meta_features.loc[:, ["index", "CVIR inter class", "Mean of kurtosis", "Bound",  "Density", "Attributes", "Average examples per labelset", "LxIxF", "Cardinality"]]



#meta_targets_BR_vs_LP = problem_transformation_vs_algortihm_adap(meta_tar)

if riseOrDown == "rise":
    scenario1_targets = meta_target_extract_larger_better(meta_tar)
    scenario2_targets = meta_target_extract_larger_better(meta_tar)
    #scenario3_targets = meta_target_extract_larger_better(meta_targets_BR_vs_LP)

    tar1 = problem_transformation_vs_algortihm_adap(scenario1_targets)
    tar2 = ensemble_vs_single_target(scenario2_targets)
    #tar3 = br_vs_lp_singletons(scenario3_targets)
    tar4 = numeric_rise(meta_tar)

else:
    scenario1_targets = meta_target_extract_smaller_better(meta_tar)
    scenario2_targets = meta_target_extract_smaller_better(meta_tar)
    scenario3_targets = meta_target_extract_smaller_better(meta_targets_BR_vs_LP)

    tar1 = problem_transformation_vs_algortihm_adap(scenario1_targets)
    tar2 = ensemble_vs_single_target(scenario2_targets)
    tar3 = br_vs_lp_singletons(scenario3_targets)
    tar4 = numeric_down(meta_tar)

from sklearn.ensemble import RandomForestClassifier

meta_learner = DecisionTreeClassifier(class_weight="balanced", presort=True, min_samples_split=0.10, max_depth=None)
#meta_learner = KNeighborsClassifier(n_neighbors=3)
#meta_learner = RandomForestClassifier(10)
#meta_learner = SVC(C=1, gamma=10, class_weight="balanced")

loocv = LeaveOneOut()

from sklearn.feature_selection import RFE

#rfe = RFE(RandomForestClassifier, 8)
meta_features_no_target = meta_features.iloc[:, 1:].values


#from sklearn.feature_selection import RFE
#model = RandomForestClassifier()
#rfe = RFE(model, 20)
#Xrfe = rfe.fit_transform(meta_features_no_target, tar1)
#model.fit(Xrfe, tar1)


meta_predictions = []


from collections import defaultdict
val_score = defaultdict(list)
test_score = defaultdict(dict)

for train_indexUp, test_indexUP in loocv.split(meta_features):
    X_tr = meta_features.iloc[train_indexUp, 1:].values
    X_ts = meta_features.iloc[test_indexUP, 1:].values
    y_tr = tar1[train_indexUp]
    y_ts = tar1[test_indexUP]

    cnt = 0
    for train_val_index, test_val_index in loocv.split(X_tr):
        #a = selecctFeatures(meta_features_no_target[train_index, :], tar1[train_index])
        #cols = list(meta_features.iloc[:, 1:].columns)
        #model = RandomForestClassifier(10)
        # Initializing RFE model
        #rfe = RFE(model, 15)
        # Transforming data using RFE
        #X_rfe = rfe.fit_transform(meta_features_no_target[train_index, :], tar1[train_index])
        # Fitting the data to model
        #model.fit(meta_features[train_index], tar1[train_index])
        #temp = pd.Series(rfe.support_, index=cols)
        #selected_features_rfe = temp[temp == True].index
        #print(selected_features_rfe)
        X_train_cv = X_tr[train_val_index, :]
        X_test_cv = X_tr[test_val_index, :]
        y_train_cv = y_tr[train_val_index]
        y_test_cv = y_tr[test_val_index]


        meta_learner.fit(X_train_cv, y_train_cv)
        prediction = meta_learner.predict(X_test_cv)

        cnt+=1

        score = accuracy_score(y_true=y_test_cv, y_pred=prediction)

        val_name = meta_features.iloc[test_val_index, 0].values[0]
        print(val_name)
        #print(cnt)
        val_score[val_name].append(score)

    meta_learner.fit(X_tr, y_tr)
    pred = meta_learner.predict(X_ts)
    test_name = meta_features.iloc[test_indexUP, 0].values[0]

    test_score[test_name] = accuracy_score(y_ts, pred)

print("The results are {} with std {}".format(pd.DataFrame(test_score, index=[0]).T.values.mean(), pd.DataFrame(test_score, index=[0]).T.values.std()))


meta_learner.fit(meta_features.iloc[:, 1:].values, tar1)

plt.figure(figsize=(16, 4))

# ax.imshow(im, aspect='auto', extent=(20, 80, 20, 80), alpha=0.5)

sktree.plot_tree(meta_learner, feature_names=meta_features.columns[1:], filled=True, rounded=True)
ax = plt.gca()
#plt.xlim(-100, 100)
plt.savefig("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task2/AlgorithmAdaptation_vs_problemTrasnformation_DecisionTree" + measure + ".png")
plt.show()

        #if score == 0:
        #    print("Evaluation for dataset {} with result on F1 score {}".format(meta_features.iloc[test_index, 0], score))
        #meta_predictions.append(score)


#print("Final score: {}".format(np.array(meta_predictions).mean()))
#print("Final score: {}".format(np.array(meta_predictions).std()))



# from sklearn.decomposition import PCA
# from sklearn.manifold import TSNE
# import matplotlib.pyplot as plt
#
# pca = TSNE(n_components=2, perplexity=5, random_state=42)
# #pca = PCA(n_components=2, random_state=42)
# components = pca.fit_transform(meta_features.loc[:, selected_features_rfe].values)
# colors = np.where(tar1==1, "red", "blue")
#
# for x in range(0, len(tar1)):
#     plt.scatter(components[x, 0], components[x, 1], c=colors[x])
#     plt.text(components[x, 0], components[x, 1], s=meta_features.iloc[x, 0])
#
# # Maybe observing the top ranked is too strong.