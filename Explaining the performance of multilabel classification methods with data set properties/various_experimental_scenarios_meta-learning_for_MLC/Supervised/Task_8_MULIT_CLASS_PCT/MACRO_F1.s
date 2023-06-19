[Data]
File = /home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_8_MULIT_CLASS_PCT/dataset_clus_MACRO_F1_.arff 
TestSet = None
PruneSet = None
XVal = 40
RemoveMissingTarget = No
NormalizeData = None

[Attributes]
Target = 52
Clustering = 52
Descriptive = 2-51

[Tree]
FTest = [0.001, 0.01, 0.1, 0.05, 0.125]
Heuristic = Gain

[Model]
ParamTuneNumberFolds = 39
MinimalWeight = 2

%[Constraints]
%Syntactic = None
%MaxSize = Infinity
%MaxError = 0.0
%MaxDepth = 100

%[Ensemble]
%Iterations = 100
%EnsembleMethod = RForest
%SelectRandomSubspaces = SQRT
%FeatureRanking = Genie3
%FeatureRankingPerTarget = Yes

[Output]
PrintModelAndExamples = Yes
ShowInfo = Key
