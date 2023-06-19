import os
import pandas as pd
import sys
import arff

settings_file  = "/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_11_times/settings_file.s"

metriccccc = ['ACCURACY_example_based', 'AUCROC_MICRO', 'AUPRC_MICRO',
              'COVARAGE', 'F1_example_based', 'HAMMING_LOSS_example_based',
              'LABEL_RANKING_AVERAGE_PRECISION', 'LABEL_RANKING_LOSS',
              'MACRO_F1', 'MACRO_PRECISION', 'MACRO_RECALL', 'MICRO_F1',
              'MICRO_PRECISION', 'MICRO_RECALL', 'ONE_ERROR',
              'PRECISION_example_based', 'RECALL_example_based',
              'SUBSET_ACCURACY', "training_time", "test_time"]


data = pd.read_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/metaDataset.csv")

training_time = pd.read_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_11_times/training_time.csv")
col = training_time.columns
v = []
for x in col:
    v.append(x.replace(" ", ""))

training_time.columns = v
real = ["RFPCT", "RFDTBR", "EBRJ48"]

from sklearn.preprocessing import minmax_scale

training_time_ = training_time.loc[:, real].values
training_time_ = ((training_time_ - training_time_.min())/(training_time_.max()-training_time_.min())).round(6)
training_time_ = pd.DataFrame(training_time_)
training_time_.columns = real

#
# data = pd.read_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_6/dataset_clus.csv")
# non_scaled = pd.concat([training_time.iloc[:, 0], training_time_], axis=1)
# non_scaled = non_scaled.reset_index()
# non_scaled = non_scaled.drop(["index"], axis=1)
#
# def process(x):
#     return x.replace("\\_", "_").replace(" ", "")
#
# metric = "test_time"
# #
# non_scaled.iloc[:, 0]= non_scaled.iloc[:, 0].apply(lambda x: process(x))
# #
# # #non_scaled = non_scaled.iloc[:, :63]
# # non_scaled.index = non_scaled.iloc[:, 0]
# non_scaled.columns = ["index", "RFPCT", "RFDTBR", "EBRJ48"]
#
#
# fin = pd.merge(data.iloc[:, :-5], non_scaled, on="index").drop_duplicates()
#
#
#
#
# fin = fin.dropna(axis=1)
#
# # d = createArff(fin.values, fin.columns)
#
# fin.to_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_11_times/dataset_clus.csv", index=False, float_format="%.5f")
#
# os.system("csv2arff dataset_clus.csv dataset_clus.arff")
#
# #
# # with open("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_8_MULIT_CLASS_PCT/dataset_clus.arff") as file:
# #     content1 = file.readlines()
# #
# # with open("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_6/dataset_clus.arff", "r+") as file:
# #     content2 = file.readlines()
# #     x = "a"
# #     cnt = 0
# #     pom_list1 = []
# #     pom_list2 = []
# #     while "@DATA" not in x:
# #         pom_list1.append(content1[cnt])
# #         cnt += 1
# #         x = pom_list1[cnt-1]
# #     cnt = 0
# #     x = "a"
# #     while "@data" not in x:
# #         pom_list2.append(content2[cnt])
# #         cnt += 1
# #         x = pom_list2[cnt-1]
# #     novel_list = []
# #
# #     for x in pom_list1:
# #         novel_list.append(x)
# #
# #     for x in range(cnt, len(content2)-1):
# #         novel_list.append(content2[x])
# #
# #     file.seek(0)
# #     file.writelines(novel_list)
#
# with open(settings_file, "r") as file:
#     content = file.readlines()
#
# new_file_name = metric + ".s"
# with open(new_file_name, "w") as file:
#    file.writelines(content)
#
# os.system("java -jar clus.jar -xval " + new_file_name)