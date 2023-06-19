import os
import pandas as pd
import sys
import arff

settings_file  = "/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_6/settings_file.s"



metriccccc = ['ACCURACY_example_based', 'AUCROC_MICRO', 'AUPRC_MICRO',
              'COVARAGE', 'F1_example_based', 'HAMMING_LOSS_example_based',
              'LABEL_RANKING_AVERAGE_PRECISION', 'LABEL_RANKING_LOSS',
              'MACRO_F1', 'MACRO_PRECISION', 'MACRO_RECALL', 'MICRO_F1',
              'MICRO_PRECISION', 'MICRO_RECALL', 'ONE_ERROR',
              'PRECISION_example_based', 'RECALL_example_based',
              'SUBSET_ACCURACY']

metric = "AUPRC_MICRO"

data = pd.read_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/metaDataset.csv")
trainSet = data[data.iloc[:, -1] == metric]

targets_do_not_delete = ['MLkNN', 'MLARM', 'DEEP1',
                           'PCT', 'BPNN', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
                           'BR', 'HOMER', 'RFDTBR', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
                           'EBRJ48', 'TREMLCnew', 'MBR', 'ECCJ48', "Ada300", 'RSMLCC', "SSM", "CDN", "RFPCT"]

targets = ['MLkNN', 'MLARM', 'DEEP1',
                           'PCT', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
                           'BR', 'HOMER', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
                           'TREMLCnew', 'MBR', 'ECCJ48', "Ada300", 'RSMLCC', "SSM", "CDN", "BPNN"]

trainSet = trainSet.drop(targets, axis=1)
trainSet = trainSet.iloc[:, 1:-1]


real = ["EBRJ48", "RFDTBR", "RFPCT"]


def createArff(csv, columns):
    d={}
    d[u"relation"]= u'metaDataset'
    d[u"data"] = csv.tolist()
    names = [(columns[0], u'STRING')]
    for x in columns[1:]:
        names.append((x, u"REAL"))
    d[u"attributes"] = names
    d[u"description"] = u""

    # print(type(d["data"]))

    file = open("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_6/dataset_clus.arff", "wb")
    arff.dumps(d, file)
    file.close()

    return d




non_scaled = pd.read_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_6/metaDataSet.csv")
non_scaled = non_scaled.loc[:, trainSet.columns[:(-1)*len(real)]]

#non_scaled = non_scaled.iloc[:, :63]
non_scaled.index = non_scaled.iloc[:, 0]
trainSet.index = trainSet.iloc[:, 0]

trainSet = trainSet.drop(["index"], axis=1).iloc[:, (-1)*len(real):]
non_scaled = non_scaled.drop(["index"], axis=1)

non_scaled = non_scaled.reset_index()
trainSet = trainSet.reset_index()
trainSet = trainSet.iloc[:, 1:]

fin = pd.concat([non_scaled, trainSet], axis=1)


fin = fin.dropna(axis=1)

# d = createArff(fin.values, fin.columns)

fin.to_csv("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_6/dataset_clus.csv", index=False)

os.system("csv2arff dataset_clus.csv dataset_clus.arff")

#
# with open("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_8_MULIT_CLASS_PCT/dataset_clus.arff") as file:
#     content1 = file.readlines()
#
# with open("/home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_6/dataset_clus.arff", "r+") as file:
#     content2 = file.readlines()
#     x = "a"
#     cnt = 0
#     pom_list1 = []
#     pom_list2 = []
#     while "@DATA" not in x:
#         pom_list1.append(content1[cnt])
#         cnt += 1
#         x = pom_list1[cnt-1]
#     cnt = 0
#     x = "a"
#     while "@data" not in x:
#         pom_list2.append(content2[cnt])
#         cnt += 1
#         x = pom_list2[cnt-1]
#     novel_list = []
#
#     for x in pom_list1:
#         novel_list.append(x)
#
#     for x in range(cnt, len(content2)-1):
#         novel_list.append(content2[x])
#
#     file.seek(0)
#     file.writelines(novel_list)

with open(settings_file, "r") as file:
    content = file.readlines()

new_file_name = metric + ".s"
with open(new_file_name, "w") as file:
   file.writelines(content)

os.system("java -jar clus.jar -xval " + new_file_name)