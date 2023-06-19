from version_control_script import *



"""
Output: Creates file containing all aglortihm configurations.
"""


from skmultilearn.ext import Meka
from skmultilearn import ensemble as ens
from skmultilearn import problem_transform as prob_tras
from skmultilearn.cluster import LabelCooccurrenceGraphBuilder, RandomLabelSpaceClusterer
from skmultilearn.ensemble import LabelSpacePartitioningClassifier
from skmultilearn.problem_transform import ClassifierChain
from sklearn.naive_bayes import GaussianNB
from skmultilearn.adapt import MLTSVM
from skmultilearn.adapt import MLARAM
from skmultilearn.adapt import MLkNN
from skmultilearn.adapt import BRkNNaClassifier
from skmultilearn.embedding import CLEMS
from sklearn.ensemble import RandomForestRegressor
from skmultilearn.embedding import EmbeddingClassifier
from sklearn.model_selection import GridSearchCV

# import base learners
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC


def CalibratedLabelRanking(setOfParameters):
    """
    :param setOfParameters: dictionary of Lists of floats; {'-C': [0.1, 0.2], '-G':[0.5, 1.0]}
    :return: list of tuples. First element of the tuple is configured CLR method. Second element of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for cost in setOfParameters['C']:
        for gamma in setOfParameters['G']:
            d = {}
            parametarizationGamma = ' -G ' +  str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                meka_classifier = 'meka.classifiers.multilabel.MULAN -threshold "PCut1" -S CLR',
                weka_classifier = 'weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -M ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -num-decimal-places 4\"',
                meka_classpath = mekaPath,
                java_command = javaPath)
            d["provides_probabilites"] = "YES"
            d["method_name"] = "Calibrated Label Ranking"
            d["library"] = "MEKA"
            d["language"] = "JAVA"
            d["family methods"] = "problem transformations"
            d["command"] = 'meka.classifiers.multilabel.MULAN  -S CLR'
            d["method_parameters"] = {"-threshold": "PCut1",
                                      "MLL_base": {"method_name": None},
                                      "baseLearner":  {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                        "parameters": {"-L":'0.001',
                                                                        "-P":"1.0E-12",
                                                                        "-N":"2",
                                                                        "-V": "-1",
                                                                        "-W":"1",
                                                                        "-C":str(cost),
                                                                        "kernel":{"kernelName":"Gaussian",
                                                                                  "parameters":{"gamma":str(gamma),
                                                                                                "-C":str(250007),
                                                                                                "-calibrator":{"name": "weka.classifiers.functions.Logistic",
                                                                                                               "-R": "1.08E-8",
                                                                                                               "-M":"-1",
                                                                                                               "-num-decimal-places":"4"}}}}}}
            configurations.append((clf, 'CalibratedLabelRanking_with_SMO_gaussian_kernel_cost_' + str(cost).replace(".", "_") + '_gamma_' + str(gamma).replace(".", "_"), d))
            parametarization = ''
            parametarizationGamma = ''
            parametarizationC = ''
    return configurations

def MetaBinaryRelevance(setOfParameters):
    """
    This method has no parameters. As base learner it SVM which we optimize.
    :return: list of tuples. First element of the tuple is configured MBR method. Second element of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for cost in setOfParameters['C']:
        for gamma in setOfParameters['G']:
            d = {}
            parametarizationGamma = ' -G ' + str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.MBR -threshold "PCut1" ',
                    weka_classifier = 'meka.classifiers.multilabel.BR -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -M -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8  -num-decimal-places 4\"',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
            d["provides_probabilites"] = "YES"
            d["method_name"] = "Meta Binary Relevance"
            d["library"] = "MEKA"
            d["language"] = "JAVA"
            d["family methods"] = "problem transformations"
            d["command"] = 'meka.classifiers.multilabel.meta.MBR -W meka.classifier.multilabel.BR'
            d["method_parameters"] = {"-threshold": "PCut1", "MLL_base": "meka.classifier.multilabel.BR", "baseLearner":
                                                                                            {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                                                             "parameters": {"-L":'0.001',
                                                                                                           "-P": "1.0E-12",
                                                                                                           "-N":"2",
                                                                                                           "-V": "-1",
                                                                                                           "-W":"1",
                                                                                                           "-C":str(cost),
                                                                                                           "kernel":{"kernelName":"Gaussian",
                                                                                                           "parameters":{"gamma":str(gamma),
                                                                                                                         "-C":str(250007),
                                                                                                                         "-calibrator":{"name": "weka.classifiers.functions.Logistic",
                                                                                                                                       "-R": "1.08E-8",
                                                                                                                                       "-M":"-1",
                                                                                                                                       "-num-decimal-places":"4"}}}}}}
            configurations.append((clf,  "MetaBinaryRelevance_with_SMO_gaussian_kernel_cost_" + str(cost).replace(".", "_") + "_gamma_" + str(gamma).replace(".", "_"), d))


            parametarization = ''
            parametarizationGamma = ''
            parametarizationC = ''
    return configurations


def EnsembleOfClassifierChains(setOfParameters):
    """
    :param setOfParameters: dictionary of Lists of floats; {'-C': [0.1, 0.2], '-G':[0.5, 1.0]}
    :return: list of tuples. First element of the tuple is configured ECC method. Second element of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for iterators in setOfParameters['I']:
        for cost in setOfParameters['C']:
            for gamma in setOfParameters['G']:
                d = {}
                parametarizationGamma = ' -G ' + str(gamma)
                parametarizationC = '-C ' + str(cost)
                parametarization = parametarizationC + " " + parametarizationGamma + " " + str(iterators)
                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.BaggingMLdup -threshold "PCut1" -S 1 -P 100 -I '+str(iterators),
                    weka_classifier='meka.classifiers.multilabel.CC -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -M ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8  -num-decimal-places 4\"',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                d["provides_probabilites"] = "YES"
                d["method_name"] = "Ensemble of Classifier Chains"
                d["library"] = "MEKA"
                d["family methods"] = "problem transformations"
                d["language"] = "JAVA"
                d["command"] = 'meka.classifiers.multilabel.meta.BaggingMLdup -W meka.classifier.multilabel.CC'
                d["method_parameters"] = {"-threshold": "PCut1",
                                          "-S": str(1),
                                          "-P": str(100),
                                          "-I": str(iterators),
                                          "MLL_base": {"method_name":"meka.classifier.multilabel.CC"},
                                          "baseLearner":
                                                        {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                        "parameters": {"-L": '0.001',
                                                                  "-P": "1.0E-12",
                                                                  "-N": "2",
                                                                  "-V": "-1",
                                                                  "-W": "1",
                                                                  "-C": str(cost),
                                                                  "kernel": {"kernelName": "Gaussian",
                                                                             "parameters": {"gamma": str(gamma),
                                                                                            "-C": str(250007),
                                                                                            "-calibrator": {
                                                                                                "name": "weka.classifiers.functions.Logistic",
                                                                                                "-R": "1.08E-8",
                                                                                                "-M": "-1",
                                                                                                "-num-decimal-places": "4"}}}}}}
                configurations.append((clf, "EsembleOfClassifierChains_with_Iterators_" + str(iterators) + "_with_SMO_gaussian_kernel_cost_" + str(cost).replace(".", "_") + "_gamma_" + str(gamma).replace(".", "_"), d))
                parametarization = ''
    return configurations


def EnsembleOfBinaryRelevance(setOfParameters):
    """
    :param setOfParameters: dictionary of Lists of floats; {'-C': [0.1, 0.2], '-G':[0.5, 1.0]}
    :return: list of tuples. First element of the tuple is configured EBR method. Second elemet of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for iterators in setOfParameters['I']:
        for cost in setOfParameters['C']:
            for gamma in setOfParameters['G']:
                d={}
                parametarizationGamma = ' -G ' + str(gamma)
                parametarizationC = '-C ' + str(cost)
                parametarization = parametarizationC + " " + parametarizationGamma + " " + str(iterators)
                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.BaggingMLdup -threshold "PCut1" -S 1 -P 100 -I '+str(iterators),
                    weka_classifier='meka.classifiers.multilabel.BR -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -M -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -num-decimal-places 4\"',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                d["provides_probabilites"] = "YES"
                d["method_name"] = "Ensemble of Binary Relevance"
                d["library"] = "MEKA"
                d["language"] = "JAVA"
                d["family methods"] = "problem transformations"
                d["command"] = 'meka.classifiers.multilabel.meta.BaggingMLdup -W meka.classifier.multilabel.BR'
                d["method_parameters"] = {"-threshold": "PCut1",
                                          "-S": str(1),

                                          "-P": str(100),
                                          "-I": str(iterators),
                                          "MLL_base": {"method_name":"meka.classifier.multilabel.BR"},
                                          "baseLearner":
                                                        {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                        "parameters": {"-L": '0.001',
                                                                  "-P": "1.0E-12",
                                                                  "-N": "2",
                                                                  "-V": "-1",
                                                                  "-W": "1",
                                                                  "-C": str(cost),
                                                                  "kernel": {"kernelName": "Gaussian",
                                                                             "parameters": {"gamma": str(gamma),
                                                                                            "-C": str(250007),
                                                                                            "-calibrator": {
                                                                                                "name": "weka.classifiers.functions.Logistic",
                                                                                                "-R": "1.08E-8",
                                                                                                "-M": "-1",
                                                                                                "-num-decimal-places": "4"}}}}}}
                configurations.append((clf, "meka_classifiers_multilabel_meta_EnsembleML_BinaryRelevance_with_Iterators" + str(iterators) + "_with_SMO_gaussian_kernel_cost_" + str(cost).replace(".", "_") + "_gamma_" + str(gamma).replace(".", "_"), d))
                parametarization = ''
    return configurations

def EnsembleOfLabelPowerSets(setOfParameters):
    """
    :param setOfParameters: dictionary of Lists of floats; {'-C': [0.1, 0.2], '-G':[0.5, 1.0]}
    :return: list of tuples. First element of the tuple is configured ELP method. Second elemet of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for iterators in setOfParameters['I']:
        for cost in setOfParameters['C']:
            for gamma in setOfParameters['G']:
                d={}
                parametarizationGamma = ' -G ' + str(gamma)
                parametarizationC = '-C ' + str(cost)
                parametarization = parametarizationC + " " + parametarizationGamma + " " + str(iterators)
                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.BaggingMLdup -threshold "PCut1" -S 1 -P 70 -I '+str(iterators),
                    weka_classifier='meka.classifiers.multilabel.LC -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -M ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8  -num-decimal-places 4\"',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                d["provides_probabilites"] = "YES"
                d["method_name"] = "Ensemble of Label PowerSets"
                d["library"] = "MEKA"
                d["family methods"] = "problem transformations"
                d["language"] = "JAVA"
                d["command"] = 'meka.classifiers.multilabel.meta.BaggingMLdup -W meka.classifier.multilabel.LC'
                d["method_parameters"] = {"-threshold": "PCut1",
                                          "-S": str(1),
                                          "-P": str(70),
                                          "-I": str(iterators),
                                          "MLL_base": {"method_name":"meka.classifier.multilabel.LC"},
                                          "baseLearner":
                                                        {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                        "parameters": {"-L": '0.001',
                                                                  "-P": "1.0E-12",
                                                                  "-N": "2",
                                                                  "-V": "-1",
                                                                  "-W": "1",
                                                                  "-C": str(cost),
                                                                  "kernel": {"kernelName": "Gaussian",
                                                                             "parameters": {"gamma": str(gamma),
                                                                                            "-C": str(250007),
                                                                                            "-calibrator": {
                                                                                                "name": "weka.classifiers.functions.Logistic",
                                                                                                "-R": "1.08E-8",
                                                                                                "-M": "-1",
                                                                                                "-num-decimal-places": "4"}}}}}}
                configurations.append((clf, "meka_classifiers_multilabel_meta_EnsembleML_PowerSets_with_Iterators" + str(iterators) + "_with_SMO_gaussian_kernel_cost_" + str(cost).replace(".", "_") + "_gamma_" + str(gamma).replace(".", "_"), d))
                parametarization = ''
    return configurations


def BinaryRelevance(setOfParameters):
    """
    :param setOfParameters: dictionary of Lists of floats; {'-C': [0.1, 0.2], '-G':[0.5, 1.0]}
    :return: list of tuples. First element of the tuple is configured BR method. Second element of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for cost in setOfParameters['C']:
        for gamma in setOfParameters['G']:
            d={}
            parametarizationGamma = ' -G ' +  str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                meka_classifier = 'meka.classifiers.multilabel.BR -threshold "PCut1"',
                weka_classifier = 'weka.classifiers.functions.SMO -- -M -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -num-decimal-places 4\"',
                meka_classpath = mekaPath,
                java_command = javaPath)
            d["provides_probabilites"] = "YES"
            d["method_name"] = "Binary Relevance"
            d["library"] = "MEKA"
            d["family methods"] = "problem transformations"
            d["language"] = "JAVA"
            d["command"] = 'meka.classifiers.multilabel.BR'
            d["method_parameters"] = {"-threshold": "PCut1",
                                      "MLL_base": {"method_name": None},
                                      "baseLearner":
                                          {"baseMethodName": 'weka.classifiers.functions.SMO',
                                           "parameters": {"-L": '0.001',
                                                          "-P": "1.0E-12",
                                                          "-N": "2",
                                                          "-V": "-1",
                                                          "-W": "1",
                                                          "-C": str(cost),
                                                          "kernel": {"kernelName": "Gaussian",
                                                                     "parameters": {"gamma": str(gamma),
                                                                                    "-C": str(250007),
                                                                                    "-calibrator": {
                                                                                        "name": "weka.classifiers.functions.Logistic",
                                                                                        "-R": "1.08E-8",
                                                                                        "-M": "-1",
                                                                                        "-num-decimal-places": "4"}}}}}}

            configurations.append((clf, "meka_classifiers_multilabel_BR_SMO_cost_" + str(cost).replace(".", "_") + "_gamma_" + str(gamma).replace(".", "_"), d))
            parametarization = ''
            parametarizationGamma = ''
            parametarizationC = ''
    return configurations


def LabelPowerSet(setOfParameters):
    """
    :param setOfParameters: dictionary of Lists of floats; {'-C': [0.1, 0.2], '-G':[0.5, 1.0]}
    :return: list of tuples. First element of the tuple is configured LP method. Second element of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for cost in setOfParameters['C']:
        for gamma in setOfParameters['G']:
            d={}
            parametarizationGamma = ' -G ' +  str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                meka_classifier = 'meka.classifiers.multilabel.LC -threshold "PCut1" ',
                weka_classifier = 'weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -M -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -num-decimal-places 4\"',
                meka_classpath = mekaPath,
                java_command = javaPath)

            d["provides_probabilites"] = "NO"
            d["method_name"] = "Label PowerSets"
            d["library"] = "MEKA"
            d["language"] = "JAVA"
            d["family methods"] = "problem transformations"
            d["command"] = 'meka.classifiers.multilabel.LC'
            d["method_parameters"] = {"-threshold": "PCut1",
                                      "MLL_base": {"method_name": None},
                                      "baseLearner":
                                          {"baseMethodName": 'weka.classifiers.functions.SMO',
                                           "parameters": {"-L": '0.001',
                                                          "-P": "1.0E-12",
                                                          "-N": "2",
                                                          "-V": "-1",
                                                          "-W": "1",
                                                          "-C": str(cost),
                                                          "kernel": {"kernelName": "Gaussian",
                                                                     "parameters": {"gamma": str(gamma),
                                                                                    "-C": str(250007),
                                                                                    "-calibrator": {
                                                                                    "name": "weka.classifiers.functions.Logistic",
                                                                                    "-R": "1.08E-8",
                                                                                    "-M": "TRUE",
                                                                                    "-num-decimal-places": "4"}}}}}}
            configurations.append((clf, "meka_classifiers_multilabel_LC_SMO_cost_" + str(cost).replace(".", "_") + "_gamma_" + str(gamma).replace(".", "_"), d))
            parametarization = ''
            parametarizationGamma = ''
            parametarizationC = ''
    return configurations

def PrunedSets(setOfParamteres):
    """
    :param setOfParameters: dictionary of Lists of floats; {'-C': [0.1, 0.2], '-G':[0.5, 1.0]}
    :return: list of tuples. First element of the tuple is configured PS method. Second element of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for pruningValue in setOfParamteres['P']:
        for maxNumberFreqLabelSets in setOfParamteres["N"]:
                for cost in setOfParamteres["C"]:
                    for gamma in setOfParamteres["G"]:

                        d = {}
                        parametarizationPruningValue = ' -P ' +  str(pruningValue)
                        parametarizationmaxNumberFreqLabelSets = ' -N ' + str(maxNumberFreqLabelSets)

                        clf = Meka(
                            meka_classifier = 'meka.classifiers.multilabel.PSt -threshold "PCut1" -S 0' + parametarizationPruningValue + parametarizationmaxNumberFreqLabelSets,
                            weka_classifier = 'weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -M  -W 1 -C ' + str(cost) + ' -K \"weka.classifiers.functions.supportVector.RBFKernel -G ' + str(gamma) + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8  -num-decimal-places 4\"',
                            meka_classpath = mekaPath,
                            java_command = javaPath)
                        d["provides_probabilites"] = "YES"
                        d["method_name"] = "Pruned Sets"
                        d["library"] = "MEKA"
                        d["language"] = "JAVA"
                        d["family methods"] = "problem transformations"
                        d["command"] = 'meka.classifiers.multilabel.PSt'
                        d["method_parameters"] = {"-threshold": "PCut1",
                                                  "-S": str(0),
                                                  "-P": str(pruningValue),
                                                  "-N": str(maxNumberFreqLabelSets),
                                                  "baseLearner":
                                                                                {
                                                                                    "baseMethodName": 'weka.classifiers.functions.SMO',
                                                                                    "parameters": {"-L": '0.001',
                                                                                                   "-P": "1.0E-12",
                                                                                                   "-N": "2",
                                                                                                   "-V": "-1",
                                                                                                   "-W": "1",
                                                                                                   "-C": str(cost),
                                                                                                   "kernel": {
                                                                                                       "kernelName": "Gaussian",
                                                                                                       "parameters": {
                                                                                                           "gamma": str(
                                                                                                               gamma),
                                                                                                           "-C": str(250007),
                                                                                                           "-calibrator": {
                                                                                                               "name": "weka.classifiers.functions.Logistic",
                                                                                                               "-R": "1.08E-8",
                                                                                                               "-M": "-1",
                                                                                                               "-num-decimal-places": "4"}}}}}}

                        configurations.append((clf, 'meka_classifiers_multilabel_PS_Seed_0_pruning_value_' + str(pruningValue) + "_maxNumberFreqLabels_" + str(maxNumberFreqLabelSets) +  "_with_Gaussian_kernel_SMO_cost_" + str(cost).replace(".", "_") + "_gamma_" + str(gamma).replace(".", "_"), d))
                parametarization = ''
                parametarizationGamma = ''
                parametarizationC = ''
    return configurations


def EnsembleOFPrunedSets(setOfParameters):
    """
    :param setOfParameters: dictionary of Lists of floats; {'-C': [0.1, 0.2], '-G':[0.5, 1.0]}
    :return: list of tuples. First element of the tuple is configured PS method. Second element of the tuple contains the description of learner in form. Meka method | Base classifier with its confguration
    """
    configurations = []
    for pruningValue in setOfParameters['P']:
        for maxNumberFreqLabelSets in setOfParameters["N"]:
            for iterators in setOfParameters['I']:
                parametarizationPruningValue = ' -P ' +  str(pruningValue)
                parametarizationmaxNumberFreqLabelSets = ' -N ' + str(maxNumberFreqLabelSets)
                parametarizationIterators = ' -I ' + str(iterators)
                d = {}
                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.EnsembleML -threshold "PCut1" -S 1 -P 70 -I '+str(iterators),
                    weka_classifier = 'meka.classifiers.multilabel.PS -- -S 0' + parametarizationPruningValue + parametarizationmaxNumberFreqLabelSets + ' -W weka.classifiers.trees.J48 -- -U -M 2',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                d["provides_probabilites"] = "YES"
                d["family methods"] = "problem transformations"
                d["method_name"] = "Ensemble of Pruned Sets"
                d["library"] = "MEKA"
                d["language"] = "JAVA"
                d["command"] = 'meka.classifiers.multilabel.meta.EnsembleML'
                d["method_parameters"] = {"-threshold": "PCut1",
                                          "-S": "1",
                                          "-P": "70",
                                          "-I": str(iterators),
                                          "MLL_base": {"method_name": "meka.classifiers.multilabel.PS"},
                                                       "method_parameters": {"-S": str(0),
                                                                             "-P": str(pruningValue),
                                                                             "-N": str(maxNumberFreqLabelSets)},

                                          "baseLearner":
                                                      {"baseMethodName": 'weka.classifiers.trees.J48',
                                                       "parameters": {"-M": str(2),
                                                                      "-U": "True",
                                                                      "-C": "0.25"}}}
                configurations.append((clf, 'meka_classifiers_multilabel_meta_EnsembleML_with_Iterators'+ str(iterators) + ' meka_classifiers_multilabel_PS pruning_value' + str(pruningValue) +"_maxNUmberFreqLabelSets_" + str(maxNumberFreqLabelSets) + parametarizationIterators + ' weka_classifiers_trees_J48', d))

    return configurations


def RAkEL1(setOfParameters, targetIndex):
    """
    FIX the number of models to 10. Sets the pruning value to half of the number of labels
    :param setOfParameters:
    :param targetIndex:
    :return:
    """
    configurations = []
    for cost in setOfParameters["cost"]:
        for gamma in setOfParameters["gamma"]:
                    q = 0
                    d = {}
                    clf = Meka(
                        meka_classifier='meka.classifiers.multilabel.MULAN -S RAkEL1 -threshold "PCut1"',
                        weka_classifier='weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -M -C ' + str(cost) + ' -K \"weka.classifiers.functions.supportVector.RBFKernel -G ' + str(gamma) + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -num-decimal-places 4\"',
                        #weka_classifier='weka.classifiers.trees.J48',
                        meka_classpath=mekaPath,
                        java_command=javaPath)
                    d["provides_probabilites"] = "YES"
                    d["method_name"] = "RAkEL"
                    d["library"] = "MEKA"
                    d["language"] = "JAVA"
                    d["family methods"] = "problem transformations"
                    d["command"] = 'meka.classifiers.multilabel.MULAN'
                    d["method_parameters"] = {"-threshold": "PCut1",
                                              "-S": "RAkEL1",
                                              "MLL_base": {"method_name": None},
                                              "baseLearner":
                                                  {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                   "parameters": {"-L": '0.001',
                                                                  "-P": "1.0E-12",
                                                                  "-N": "2",
                                                                  "-V": "-1",
                                                                  "-W": "1",
                                                                  "-C": str(cost),
                                                                  "kernel": {"kernelName": "Gaussian",
                                                                             "parameters": {"gamma": str(gamma),
                                                                                            "-C": str(250007),
                                                                                            "-calibrator": {
                                                                                                "name": "weka.classifiers.functions.Logistic",
                                                                                                "-R": "1.08E-8",
                                                                                                "-M": "-1",
                                                                                                "-num-decimal-places": "4"}}}}}}
                    configurations.append((clf, "RAkel_cost_" + str(cost).replace(".", "__") + "_gamma_" + str(gamma).replace(".", "__") + "_numberOfModels_" + str(10) + "_pruning_value_" + str(int(targetIndex/2)) + "_subsambpling_value_"+str(q), d ))
    return configurations

def RAkEL2(setOfParameters, targetIndex):
    configurations = []
    for cost in setOfParameters["cost"]:
        for gamma in setOfParameters["gamma"]:
            for k in setOfParameters["labelSubspaceSize"]:
                for pv in setOfParameters["pruningValue"]:
                    numberModels = min(100, 2 * targetIndex)
                    for c in [10, numberModels]:
                        q = 0
                        d = {}

                        clf = Meka(
                            meka_classifier='meka.classifiers.multilabel.RAkEL -threshold "PCut1" -S 0 -M ' + str(c) + " -k " + str(k)+" -P " + str(pv) + " -N " + str(q),
                            weka_classifier='weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -M -C ' + str(cost) + ' -K \"weka.classifiers.functions.supportVector.RBFKernel -G ' + str(gamma) + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8  -num-decimal-places 4\"',
                            #weka_classifier='weka.classifiers.trees.J48',
                            meka_classpath=mekaPath,
                            java_command=javaPath)
                        d["provides_probabilites"] = "provide votes"
                        d["method_name"] = "RAkEL"
                        d["library"] = "MEKA"
                        d["language"] = "JAVA"
                        d["family methods"] = "problem transformations"
                        d["command"] = 'meka.classifiers.multilabel.RAkEL'
                        d["method_parameters"] = {"-threshold": "PCut1",
                                                  "-M": str(c),
                                                  "-P": str(pv),
                                                  "-k": str(k),
                                                  "-N": str(q),
                                                  "MLL_base": {"method_name": None},
                                                  "baseLearner":
                                                      {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                       "parameters": {"-L": '0.001',
                                                                      "-P": "1.0E-12",
                                                                      "-N": "2",
                                                                      "-V": "-1",
                                                                      "-M": "TRUE",
                                                                      "-W": "1",
                                                                      "-C": str(cost),
                                                                      "kernel": {"kernelName": "Gaussian",
                                                                                 "parameters": {"gamma": str(gamma),
                                                                                                "-C": str(250007),
                                                                                                "-calibrator": {
                                                                                                    "name": "weka.classifiers.functions.Logistic",
                                                                                                    "-R": "1.08E-8",
                                                                                                    "-M": "-1",
                                                                                                    "-num-decimal-places": "4"}}}}}}
                        configurations.append((clf, "RAkel_cost_" + str(cost).replace(".", "__") + "_gamma_" + str(gamma).replace(".", "__") + "_labePowerSetSize_" + str(k) + "_numberOfModels_" + str(c) + "_pruning_value_" + str(pv) + "_subsambpling_value_"+str(q), d ))
    return configurations



def RAkEL_MEKA(setOfParameters, targetIndex):
    configurations = []
    for cost in setOfParameters["cost"]:
        for gamma in setOfParameters["gamma"]:
            for k in setOfParameters["labelSubspaceSize"]:
                for pv in setOfParameters["pruningValue"]:
                    q = 0
                    d = {}
                    numberModels = min(100, 2*targetIndex)
                    clf = Meka(
                        meka_classifier='meka.classifiers.multilabel.RAkEL -threshold "PCut1" -S 0 -M ' + str(numberModels) + " -k " + str(k)+" -P " + str(pv) + " -N " + str(q),
                        weka_classifier='weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -M -C ' + str(cost) + ' -K \"weka.classifiers.functions.supportVector.RBFKernel -G ' + str(gamma) + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8  -num-decimal-places 4\"',
                        #weka_classifier='weka.classifiers.trees.J48',
                        meka_classpath=mekaPath,
                        java_command=javaPath)
                    d["provides_probabilites"] = "provide votes"
                    d["method_name"] = "RAkEL"
                    d["library"] = "MEKA"
                    d["language"] = "JAVA"
                    d["family methods"] = "problem transformations"
                    d["command"] = 'meka.classifiers.multilabel.RAkEL'
                    d["method_parameters"] = {"-threshold": "PCut1",
                                              "-M": str(numberModels),
                                              "-P": str(pv),
                                              "-k": str(k),
                                              "-N": str(q),
                                              "MLL_base": {"method_name": None},
                                              "baseLearner":
                                                  {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                   "parameters": {"-L": '0.001',
                                                                  "-P": "1.0E-12",
                                                                  "-N": "2",
                                                                  "-V": "-1",
                                                                  "-W": "1",
                                                                  "-C": str(cost),
                                                                  "kernel": {"kernelName": "Gaussian",
                                                                             "parameters": {"gamma": str(gamma),
                                                                                            "-C": str(250007),
                                                                                            "-calibrator": {
                                                                                                "name": "weka.classifiers.functions.Logistic",
                                                                                                "-R": "1.08E-8",
                                                                                                "-M": "-1",
                                                                                                "-num-decimal-places": "4"}}}}}}
                    configurations.append((clf, "RAkel_cost_" + str(cost).replace(".", "__") + "_gamma_" + str(gamma).replace(".", "__") + "_labePowerSetSize_" + str(k) + "_numberOfModels_" + str(numberModels) + "_pruning_value_" + str(pv) + "_subsambpling_value_"+str(q), d ))
    return configurations


def BackPropagationNeuralNetwork(setOfParameters):
    configurations = []
    for hidden in setOfParameters["hidden"]:
        for epoaches in setOfParameters["epoches"]:
            for learningRate in setOfParameters["learningRate"]:
                d = {}
                clf = Meka(
                    meka_classifier='meka.classifiers.multilabel.BPNN -threshold "PCut1" -m 0.2 -H ' + str(hidden) + " -E " + str(epoaches) +" -r " +str(learningRate),
                    #weka_classifier='weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -C ' + str(cost) + ' -K \"weka.classifiers.functions.supportVector.RBFKernel -G ' + str(gamma) + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"',
                    weka_classifier='weka.classifiers.trees.J48',
                    meka_classpath=mekaPath,
                    java_command=javaPath)
                d["family methods"] = "method adaptation"
                d["provides_probabilites"] = "YES"
                d["method_name"] = "ML Back propagation Neural Network"
                d["library"] = "MEKA"
                d["language"] = "JAVA"
                d["command"] = 'meka.classifiers.multilabel.BPNN'
                d["method_parameters"] = {"-threshold": "PCut1",
                                          "-m": str(0.2),
                                          "-H": str(hidden),
                                          "-E": str(epoaches),
                                          "-r": str(learningRate),
                                          "MLL_base": {"method_name": None},
                                          "baseLearner": {"baseMethodName": 'weka.classifiers.trees.J48',
                                                          "parameters": {"-M": str(2),
                                                           "-C": "0.25"}}}

                configurations.append((clf, "BPNN_hidden_units_" + str(hidden) + "_epoaches_" + str(epoaches) + "_learning_rate_"+str(learningRate).replace(".", "__")+"_baseLearner_j48_", d))  # use J48 beacause it is easier to be trained
    return configurations

def ClassifierChains(setOfParameters):
    configurations = []
    for cost in setOfParameters['C']:
        for gamma in setOfParameters['G']:
            d = {}
            parametarizationGamma = ' -G ' +  str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                meka_classifier = 'meka.classifiers.multilabel.CC -S 0 -threshold "PCut1"',
                weka_classifier = 'weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -M ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -num-decimal-places 4\"',
                meka_classpath = mekaPath,
                java_command = javaPath)

            d["provides_probabilites"] = "NO"
            d["method_name"] = "Classifier Chains"
            d["library"] = "MEKA"
            d["language"] = "JAVA"
            d["command"] = 'meka.classifiers.multilabel.CC'
            d["family methods"] = "problem transformations"
            d["method_parameters"] = {"-threshold": "PCut1",
                                      "-S": str(0),
                                      "MLL_base": {"method_name": None},
                                      "baseLearner":
                                                  {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                   "parameters": {"-L": '0.001',
                                                                  "-P": "1.0E-12",
                                                                  "-N": "2",
                                                                  "-V": "-1",
                                                                  "-W": "1",
                                                                  "-C": str(cost),
                                                                  "kernel": {"kernelName": "Gaussian",
                                                                             "parameters": {"gamma": str(gamma),
                                                                                            "-C": str(250007),
                                                                                            "-calibrator": {
                                                                                                "name": "weka.classifiers.functions.Logistic",
                                                                                                "-R": "1.08E-8",
                                                                                                "-M": "-1",
                                                                                                "-num-decimal-places": "4"}}}}}}

            configurations.append((clf, "meka_classifiers_multilabel_CC_SMO_cost_" + str(cost).replace(".", "_") + "_gamma_" + str(gamma).replace(".", "_"), d))
            parametarization = ''
            parametarizationGamma = ''
            parametarizationC = ''
    return configurations



def TwinMultiLabelSVM(setOfParameters):
    configurations = []
    for c_k in setOfParameters["cost"]:
        for loss in setOfParameters["lambda_param"]:
            for smoot_param in setOfParameters["smootParam"]:

                    d ={}
                    clf = MLTSVM(c_k=c_k, lambda_param=loss, sor_omega=0.2, threshold=smoot_param)

                    d["provides_probabilites"] = "NO"
                    d["method_name"] = "Multi Label Twin SVM"
                    d["library"] = "skmultilearn"
                    d["language"] = "python"
                    d["command"] = 'None'
                    d["family methods"] = "adaptations"
                    d["method_parameters"] = {"c_k": str(c_k),
                                              "sor_omega": str(smoot_param),
                                              "lambda_param": str(loss),
                                              }
                    configurations.append((clf, "TwinMLLSVM_cost_" + str(c_k) + "_loss_" + str(loss) + "_smoothing_param_" + str(smoot_param), d))
    return  configurations


def MultilabelARAM(setOfParameters):
    """
    This method requires calibration of the output.
    :param setOfParameters:
    :return:
    """

    configurations = []
    for c_k in setOfParameters["vigilance"]:
        for th in setOfParameters["threshold"]:
            d={}
            clf = MLARAM(vigilance=c_k, threshold=th)
            d["provides_probabilites"] = "YES"
            d["method_name"] = "Multi Label Hierarchical Neural Network"
            d["library"] = "skmultilearn"
            d["language"] = "python"
            d["command"] = 'None'
            d["family methods"] = "adaptations"
            d["method_parameters"] = {"vigilance": str(c_k),
                                      "threshold": str(th)}
            configurations.append((clf, "MultiLabelARAM_vigilance_"+str(c_k)+"_threshold_" +str(th), d))

    return  configurations


def MLkNearestNeighbour(setOfParameters):
    configurations = []

    for k in setOfParameters["k"]:
        clf = MLkNN(k=k)
        d = {}
        d["provides_probabilites"] = "YES"
        d["method_name"] = "Multi-label nearest neighbour classifier"
        d["library"] = "skmultilearn"
        d["language"] = "python"
        d["command"] = 'None'
        d["family methods"] = "adaptations"
        d["method_parameters"] = {"k_number_of_neighbours": str(k)}
        configurations.append((clf, "MLkNearestNeighbour_k_" + str(k), d))

    return  configurations
#clf = adaptation.BRkNNbClassifier(k=10)


def BRkNearestNeighbour(setOfParameters):
    configurations = []
    for k in setOfParameters["k"]:
        clf = BRkNNaClassifier(k=k)
        d = {}
        d["provides_probabilites"] = "provides confidences"
        d["method_name"] = "BRkNearestNeighbour a-version"
        d["library"] = "skmultilearn"
        d["language"] = "python"
        d["command"] = 'None'
        d["family methods"] = "adaptations"
        d["method_parameters"] = {"k_number_of_neighbours": str(k)}
        configurations.append((clf, "BR_k_NearestNeighbour_k_" + str(k), d))

    return configurations

from sklearn.metrics import hamming_loss

def CostSensitiveLabelEmbedding(setOfParameters):
    configurations = []
    for k in setOfParameters["k"]:
        clf = EmbeddingClassifier(embedder=CLEMS(hamming_loss, True), regressor=RandomForestRegressor(n_estimators=30, max_features="sqrt"), classifier=MLkNN(k=k), regressor_per_dimension=True)
        d = {}
        d["provides_probabilites"] = "YES"
        d["method_name"] = "Cost senstive Label embedding"
        d["library"] = "skmultilearn"
        d["language"] = "python"
        d["command"] = 'None'
        d["family methods"] = "embeddings"
        d["method_parameters"] = {"k_number_of_neighbours": str(k),
                                  "regression": "RandomForestRegression_30estimators_SqrtNumberOfFeatures",
                                  "regressionPerDimension":"True",
                                  "embedder":"CLEMS"}
        configurations.append((clf, "CLMES_embedding_with_random_forest_regression_30_estimators_and_MlKNN_classifier_k_"+str(k), d))
    return configurations

def RandomSubspaces_CC(setOfParameters):
    "both are LC. THE DIFFERENCE IS IN THE BASE LEARNERN NOT THE MULTI LABEL ONE"
    configurations = []
    for iterations in setOfParameters['iterations']:
        for attributes in setOfParameters["attributes"]:
            for cnf in setOfParameters["confidence"]:
                d= {}
                clf = Meka(
                    meka_classifier='meka.classifiers.multilabel.meta.RandomSubspaceML -threshold "PCut1" -P 67 -S 0 -A ' + str(attributes) + ' -I ' + str(iterations) + ' ',
                    weka_classifier='meka.classifiers.multilabel.LC -- -W weka.classifiers.trees.J48 -- -C '+ str(cnf),
                    meka_classpath=mekaPath,
                    java_command=javaPath)

                d["provides_probabilites"] = "provides votes"
                d["method_name"] = "Random Label Subpspace"
                d["library"] = "MEKA"
                d["language"] = "JAVA"
                d["command"] = 'meka.classifiers.multilabel.meta.RandomSubspaceML'
                d["family methods"] = "problem transformations"
                d["method_parameters"] = {"-threshold": "PCut1",
                                          "-A": str(attributes),
                                          "-P": "67",
                                          "-S": "0",
                                          "-I": str(iterations),
                                          "MLL_base": {"method_name": "meka.classifiers.multilabel.LC"},
                                          "method_parameters": {"-S": str(0)},
                                          "baseLearner":
                                                               {"baseMethodName": 'weka.classifiers.trees.J48',
                                                                    "parameters": {"-M": str(2),
                                                                            "-C": str(cnf),
                                                                            }}}
                configurations.append((clf, "meka_classifiers_multilabel_meta_RandomSubspaceML_with_attributes_" + str(attributes) + 'numberOfIterators_' + str(iterations) + "_LC_J48_" + "_confidence_" + str(cnf), d ))

    return configurations

def RandomSubspaces_LP(setOfParameters):
    "both are LC. THE DIFFERENCE IS IN THE BASE LEARNERN NOT THE MULTI LABEL ONE"
    configurations = []
    for iterations in setOfParameters['iterations']:
        for attributes in setOfParameters["attributes"]:
            for cost in setOfParameters["cost"]:
                for gamma in setOfParameters["gamma"]:
                    d= {}
                    clf = Meka(
                        meka_classifier='meka.classifiers.multilabel.meta.RandomSubspaceML -threshold "PCut1" -P 67 -S 0 -A ' + str(attributes) + ' -I ' + str(iterations)+ ' ',
                        weka_classifier='meka.classifiers.multilabel.LC -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -M -C ' + str(cost) + ' -K \"weka.classifiers.functions.supportVector.RBFKernel -G ' + str(gamma) + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -num-decimal-places 4\"',
                        meka_classpath=mekaPath,
                        java_command=javaPath)

                    d["provides_probabilites"] = "provides votes"
                    d["method_name"] = "Random Label Subpspace"
                    d["library"] = "MEKA"
                    d["language"] = "JAVA"
                    d["command"] = 'meka.classifiers.multilabel.meta.RandomSubspaceML'
                    d["family methods"] = "problem transformations"
                    d["method_parameters"] = {"-threshold": "PCut1",
                                              "-A": str(attributes),
                                              "-P": "67",
                                              "-S": "0",
                                              "-I": str(iterations),
                                              "MLL_base": {"method_name": "meka.classifiers.multilabel.LC"},
                                              "method_parameters": {"-S": str(0)},
                                              "baseLearner":
                                                  {"baseMethodName": 'weka.classifiers.functions.SMO',
                                                   "parameters": {"-L": '0.001',
                                                                  "-P": "1.0E-12",
                                                                  "-N": "2",
                                                                  "-V": "-1",
                                                                  "-W": "1",
                                                                  "-C": str(cost),
                                                                  "kernel": {"kernelName": "Gaussian",
                                                                             "parameters": {"gamma": str(gamma),
                                                                                            "-C": str(250007),
                                                                                            "-calibrator": {
                                                                                                "name": "weka.classifiers.functions.Logistic",
                                                                                                "-R": "1.08E-8",
                                                                                                "-M": "-1",
                                                                                                "-num-decimal-places": "4"}}}}}}

                    configurations.append((clf, "meka_classifiers_multilabel_meta_RandomSubspaceML_with_baseLearner_LC__with_attributes_" + str(attributes) + '_numberOfIterators_' + str(iterations) + "_SMO_Gaussian_cost_"+str(cost)+"_gamma_"+ str(gamma), d ))

    return configurations

def HierarchyOMER(setOfParameters):
    configurations = []

    for cost in setOfParameters["cost"]:
        for gamma in setOfParameters["gamma"]:
            for k in setOfParameters["clusters"]:
                d = {}
                clf = Meka(
                    meka_classifier='meka.classifiers.multilabel.MULAN -S HOMER.BalancedClustering.' + str(k)+".LabelPowerset -threshold \"PCut1\"",
                weka_classifier = 'weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -C ' + str(cost) + ' -K \"weka.classifiers.functions.supportVector.RBFKernel -G ' + str(gamma) + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -num-decimal-places 4\"',
                meka_classpath=mekaPath,
                java_command=javaPath)

                d["provides_probabilites"] = "YES"
                d["method_name"] = "Hierarchy of Multilabel Classifiers"
                d["library"] = "MEKA"
                d["language"] = "JAVA"
                d["command"] = 'meka.classifiers.multilabel.MULAN -S HOMER'
                d["family methods"] = "problem transformations"
                d["method_parameters"] = {"-threshold": "PCut1",
                                          "-S": str(0),
                                          "MLL_base": {"method_name": "meka.classifiers.multilabel.LC"},
                                          "baseLearner":
                                              {"baseMethodName": 'weka.classifiers.functions.SMO',
                                               "parameters": {"-L": '0.001',
                                                              "-P": "1.0E-12",
                                                              "-N": "2",
                                                              "-V": "-1",
                                                              "-W": "1",
                                                              "-C": str(cost),
                                                              "kernel": {"kernelName": "Gaussian",
                                                                         "parameters": {"gamma": str(gamma),
                                                                                        "-C": str(250007),
                                                                                        "-calibrator": {
                                                                                                              "name": "weka.classifiers.functions.Logistic",
                                                                                                              "-R": "1.08E-8",
                                                                                                              "-M": "-1",
                                                                                                                "-num-decimal-places": "4"}}}}}}
                configurations.append((clf, "HOMER_BALANCED_CLUSTERING_SVM with clusters "+str(k)+" cost "+str(cost)+ " gamma " +str(gamma), d))

    return configurations

def SubSetMapper():
    configurations = []
    d = {}
    clf = Meka(
            meka_classifier='meka.classifiers.multilabel.meta.SubsetMapper',
            weka_classifier='meka.classifiers.multilabel.BR -- -W weka.classifiers.trees.J48',
            meka_classpath=mekaPath,
            java_command=javaPath)

    d["provides_probabilites"] = "/"
    d["method_name"] = "SubSetMapper"
    d["library"] = "skmultilearn"
    d["language"] = "python"
    d["command"] = 'meka.classifiers.multilabel.meta.SubsetMapper'
    d["family methods"] = "problem transformations"
    d["method_parameters"] = {     "MLL_base": {"method_name": "meka.classifiers.multilabel.BR"},
                              "method_parameters": {"-S": str(0)},
                              "baseLearner":
                                  {"baseMethodName": 'weka.classifiers.trees.J48',
                                   "parameters": {"-M": str(2),
                                                  "-U": "True",
                                                  }}}

    configurations.append((clf, "SubsetMapperBinaryRelevance_J48", d))
    return configurations

def ConditionalDependencyNetwork(setOfParameters):
    configurations = []
    for iterations in setOfParameters["I"]:
        for collectionIterations in setOfParameters["Ic"]:
            d = {}
            clf = Meka(
            meka_classifier='meka.classifiers.multilabel.CDN -S 0 -I ' + str(iterations) + " -Ic " + str(collectionIterations) + ' ',
            weka_classifier='weka.classifiers.trees.J48',
            meka_classpath=mekaPath,
            java_command=javaPath)

            d["provides_probabilites"] = "YES"
            d["method_name"] = "SubSetMapper"
            d["library"] = "skmultilearn"
            d["language"] = "python"
            d["command"] = 'meka.classifiers.multilabel.meta.SubsetMapper'
            d["family methods"] = "problem transformations"
            d["method_parameters"] = {"-threshold": "PCut1",
                                      "-I": str(iterations),
                                      "-Ic": str(collectionIterations),
                                      "MLL_base": {"method_name": "None"},
                                      "method_parameters": {"-S": str(0)},
                                      "baseLearner":
                                          {"baseMethodName": 'weka.classifiers.trees.J48',
                                           "parameters": {"-M": str(2),
                                                          "-U": "True",
                                                          }}}

            configurations.append((clf, "ConditionalDependecyNetwork_I_" + str(iterations) + "_Ic_" + str(collectionIterations) + ' ', d))
    return  configurations



def OpenNetworkEmbedder(setOfParamters, targetIndex):
    from skmultilearn.embedding import OpenNetworkEmbedder
    from skmultilearn.cluster import LabelCooccurrenceGraphBuilder

    configurations = []
    for k in setOfParamters["k"]:
        graph_builder = LabelCooccurrenceGraphBuilder(weighted=True, include_self_edges=False)
        openne_line_params = dict(batch_size=1000, negative_ratio=5)

        if np.abs(targetIndex)%2 == 1:
            targetIndex = np.abs(targetIndex) - 1
            print(targetIndex)

        embedder = OpenNetworkEmbedder(graph_builder, embedding="LaplacianEigenmaps",  dimension=4, aggregation_function='add', normalize_weights=True)

        clf = EmbeddingClassifier(OpenNetworkEmbedder(graph_builder, 'LINE', 4, 'add', True, openne_line_params),
            RandomForestRegressor(n_estimators=30),
            MLkNN(k=k))
        #clf = EmbeddingClassifier(regressor=RandomForestRegressor(n_estimators=10), classifier=MLkNN(k=k), embedder=embedder)

        d = {}
        d["provides_probabilites"] = "YES"
        d["method_name"] = "OpenNetworkEmbedder_with_LaplacianEigenMAPS"
        d["library"] = "skmultilearn"
        d["language"] = "python"
        d["command"] = 'None'
        d["family methods"] = "embedding"
        d["method_parameters"] = {"k_number_of_neighbours": str(k),
                                  "regression": "RandomForestRegression_30estimators_SqrtNumberOfFeatures",
                                  "regressionPerDimension":"True",
                                  "embedder":"LaplacianEigenMaps"}

        configurations.append((clf, "OpenNetworkEmbedder_number_neighbours_k_" + str(k), d))

    return  configurations