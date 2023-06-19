
[Data]
File = /home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/UnsupervisedLearningScenario/descriptive_metaFeatures_not_scaled.arff
TestSet = None
PruneSet = None
XVal = 10
RemoveMissingTarget = No
NormalizeData = None

[Attributes]
Target = 2-50
Clustering = 2-50
Descriptive = 2-50
Key = 1

[Tree]
FTest = [0.001, 0.01, 0.1, 0.125]

[Model]
ParamTuneNumberFolds = 3
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
