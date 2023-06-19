[Data]
File = toClus.arff
TestSet = None
PruneSet = None
XVal = 10
RemoveMissingTarget = No
NormalizeData = None


[Attributes]
Target = 1-63
Clustering = 1-63
Descriptive = 1-63
Key = 64

Weights = Normalize

[Tree]
FTest = [0.125,0.1,0.05,0.01,0.005,0.001]

[Model]
ParamTuneNumberFolds =


%[Constraints]
%Syntactic = None
%MaxSize = Infinity
%MaxError = 0.0
%MaxDepth = 100



[Ensemble]
Iterations = 100
EnsembleMethod = RForest
SelectRandomSubspaces = SQRT
FeatureRanking = Genie3
FeatureRankingPerTarget = Yes


[Output]
ShowInfo = Count
