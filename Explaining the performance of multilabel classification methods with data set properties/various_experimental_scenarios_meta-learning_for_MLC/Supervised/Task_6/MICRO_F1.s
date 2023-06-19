[Data]
File = /home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/Supervised/Task_6/dataset_clus.arff
TestSet = None
PruneSet = None
XVal = 40
RemoveMissingTarget = No
NormalizeData = None

[Attributes]
Target = 52-54
Clustering = 52-54
Descriptive = 2-51
Key = 1

[Tree]
FTest = [0.001, 0.01, 0.1, 0.05, 0.125]

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
