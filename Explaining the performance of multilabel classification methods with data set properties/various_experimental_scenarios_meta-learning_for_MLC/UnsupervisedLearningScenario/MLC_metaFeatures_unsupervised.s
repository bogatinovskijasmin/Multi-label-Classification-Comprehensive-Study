[Data]
File = /home/matilda/PycharmProjects/MetaLearningForMLC/Meta_learning_MLC/LearningScenarios/UnsupervisedLearningScenario/descriptive_metaFeatures.arff
TestSet = None
PruneSet = None
XVal = 10
RemoveMissingTarget = No
NormalizeData = None

[Attributes]
Target = 2-51
Clustering = 2-51
Descriptive = 2-51
Key = 1

[Tree]
FTest = 0.1

[Model]
ParamTuneNumberFolds = 3

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
