from version_control_script import *



"""
Output: Creates file containing all aglortihm configurations.
"""


from skmultilearn.ext import Meka
from skmultilearn import ensemble as ens
from  skmultilearn import problem_transform as prob_tras
from skmultilearn.cluster import LabelCooccurrenceGraphBuilder, RandomLabelSpaceClusterer
from skmultilearn.ensemble import LabelSpacePartitioningClassifier
from skmultilearn.problem_transform import ClassifierChain
from sklearn.naive_bayes import GaussianNB

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
            parametarizationGamma = ' -G ' +  str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                meka_classifier = 'meka.classifiers.multilabel.MULAN -S CLR',
                weka_classifier = 'weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"',
                meka_classpath = mekaPath,
                java_command = javaPath)
            configurations.append((clf, 'meka.classifiers.multilabel.MULAN -S CLR ' + '| weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"'))
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
            parametarizationGamma = ' -G ' + str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.MBR',
                    weka_classifier = 'meka.classifiers.multilabel.BR -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
            configurations.append((clf,  'meka.classifiers.multilabel.meta.MBR' + '| meka.classifiers.multilabel.BR -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"'))
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
                parametarizationGamma = ' -G ' + str(gamma)
                parametarizationC = '-C ' + str(cost)
                parametarization = parametarizationC + " " + parametarizationGamma + " " + str(iterators)
                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.EnsembleML -S 1 -P 70 -I '+str(iterators),
                    weka_classifier='meka.classifiers.multilabel.CC -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                configurations.append((clf, 'meka.classifiers.multilabel.meta.EnsembleML -S 1 -P 70 -I ' + str(iterators) + '| meka.classifiers.multilabel.CC -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"'))
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
                parametarizationGamma = ' -G ' + str(gamma)
                parametarizationC = '-C ' + str(cost)
                parametarization = parametarizationC + " " + parametarizationGamma + " " + str(iterators)
                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.EnsembleML -S 1 -P 70 -I '+str(iterators),
                    weka_classifier='meka.classifiers.multilabel.BR -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                configurations.append((clf, 'meka.classifiers.multilabel.meta.EnsembleML -S 1 -P 70 -I ' + str(iterators) + '| meka.classifiers.multilabel.BR -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"'))
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
                parametarizationGamma = ' -G ' + str(gamma)
                parametarizationC = '-C ' + str(cost)
                parametarization = parametarizationC + " " + parametarizationGamma + " " + str(iterators)
                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.EnsembleML -S 1 -P 70 -I '+str(iterators),
                    weka_classifier='meka.classifiers.multilabel.LC -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                configurations.append((clf, 'meka.classifiers.multilabel.meta.EnsembleML -S 1 -P 70 -I ' + str(iterators) + '| meka.classifiers.multilabel.LC -- -W weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"'))
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
            parametarizationGamma = ' -G ' +  str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                meka_classifier = 'meka.classifiers.multilabel.BR',
                weka_classifier = 'weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"',
                meka_classpath = mekaPath,
                java_command = javaPath)
            configurations.append((clf, 'BinaryRelevance_SMO_gaussian_cost_' + parametarizationC + '_gamma_' + parametarizationGamma))
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
            parametarizationGamma = ' -G ' +  str(gamma)
            parametarizationC = '-C ' + str(cost)
            parametarization = parametarizationC + " " + parametarizationGamma
            clf = Meka(
                meka_classifier = 'meka.classifiers.multilabel.LC',
                weka_classifier = 'weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"',
                meka_classpath = mekaPath,
                java_command = javaPath)
            configurations.append((clf, 'meka.classifiers.multilabel.LC' + '| weka.classifiers.functions.SMO -- -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 ' + parametarizationC + ' -K \"weka.classifiers.functions.supportVector.RBFKernel ' + parametarizationGamma + ' -C 250007\" \"-calibrator\" \"weka.classifiers.functions.Logistic -R 1.08E-8 -M -1 -num-decimal-places 4\"'))
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
            for minNumberInstancesPerLeaf in setOfParamteres['M']:
                parametarizationPruningValue = ' -P ' +  str(pruningValue)
                parametarizationmaxNumberFreqLabelSets = ' -N ' + str(maxNumberFreqLabelSets)
                parametarizationminNumberInstancesPerLeaf = ' -M ' + str(minNumberInstancesPerLeaf)

                parametarization = parametarizationPruningValue + " " + parametarizationmaxNumberFreqLabelSets + " " + parametarizationminNumberInstancesPerLeaf + parametarizationmaxNumberFreqLabelSets
                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.PS -S 0' + parametarizationPruningValue + parametarizationmaxNumberFreqLabelSets,
                    weka_classifier = 'weka.classifiers.trees.J48 -- ' +parametarizationminNumberInstancesPerLeaf,
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                configurations.append((clf, 'meka.classifiers.multilabel.PS -S 0' + parametarizationPruningValue + parametarizationmaxNumberFreqLabelSets + 'weka.classifiers.trees.J48' +parametarizationminNumberInstancesPerLeaf))
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

                clf = Meka(
                    meka_classifier = 'meka.classifiers.multilabel.meta.EnsembleML -S 1 -P 70 -I '+str(iterators),
                    weka_classifier = 'meka.classifiers.multilabel.PS -- -S 0' + parametarizationPruningValue + parametarizationmaxNumberFreqLabelSets + ' -W weka.classifiers.trees.J48 -- -U -M 2',
                    meka_classpath = mekaPath,
                    java_command = javaPath)
                configurations.append((clf, 'meka.classifiers.multilabel.meta.EnsembleML -S 1 -P 70 -I '+ str(iterators) + ' meka.classifiers.multilabel.PS -S 0 ' + parametarizationPruningValue + parametarizationmaxNumberFreqLabelSets + parametarizationIterators + ' weka.classifiers.trees.J48'))

    return configurations


"""
clf = Meka(
        meka_classifier = 'meka.classifiers.multilabel.meta.EnsembleML -I 10 -P 70 ',
        weka_classifier = 'meka.classifiers.multilabel.CC -- -W weka.classifiers.functions.SMO -- -K "weka.classifiers.functions.supportVector.RBFKernel -C 10 -G 0.01"',
        meka_classpath = mekaPath,
        java_command = javaPath)
"""


## MEKA CALL OF MBR with SMO kernel RBF
#clf = Meka(
#        meka_classifier = 'meka.classifiers.multilabel.meta.MBR',
#        weka_classifier = 'meka.classifiers.multilabel.BR -- -W weka.classifiers.functions.SMO -- -K "weka.classifiers.functions.supportVector.RBFKernel -C 10 -G 0.01"',
#        meka_classpath = mekaPath,
#        java_command = javaPath)

# MEKA CALL MBR with Tree J48
#clf = Meka(
#        meka_classifier = 'meka.classifiers.multilabel.meta.MBR',
#        weka_classifier = 'meka.classifiers.multilabel.BR -- -W weka.classifiers.trees.J48',
#        meka_classpath = mekaPath,
#        java_command = javaPath)

## MEKA CALL EBR
#clf = Meka(
#        meka_classifier = 'meka.classifiers.multilabel.meta.EnsembleML -I 10 -P 70 ',
#        weka_classifier = 'meka.classifiers.multilabel.BR -- -W weka.classifiers.functions.SMO -- -K "weka.classifiers.functions.supportVector.RBFKernel -C 10 -G 0.01"',
#        meka_classpath = mekaPath,
#        java_command = javaPath)

# MEKA CALL WITH SMO KERNEL, better to use with J48
#clf = Meka(
#        meka_classifier = 'meka.classifiers.multilabel.LC',
#        weka_classifier = 'weka.classifiers.functions.SMO -- -K "weka.classifiers.functions.supportVector.RBFKernel -C 10 -G 0.01"',
#        meka_classpath = mekaPath,
#        java_command = javaPath)


# MEKA CALL  LC better to use with J48
#clf = Meka(
#        meka_classifier = 'meka.classifiers.multilabel.LC',
#        weka_classifier = 'weka.classifiers.trees.J48',
#        meka_classpath = mekaPath,
#        java_command = javaPath)

# MEKA CALL PS
#clf = Meka(
#        meka_classifier = 'meka.classifiers.multilabel.PS -P 1 -N 1',
#        weka_classifier = 'weka.classifiers.trees.J48',
#        meka_classpath = mekaPath,
#        java_command = javaPath)

# MEKA CALL PS
#clf = Meka(
#        meka_classifier = 'meka.classifiers.multilabel.meta.EnsembleML -I 10 -P 70 ',
#        weka_classifier = 'meka.classifiers.multilabel.PS -- -W weka.classifiers.functions.SMO -- -K "weka.classifiers.functions.supportVector.RBFKernel -C 10 -G 0.01"',
#        meka_classpath = mekaPath,
#        java_command = javaPath)

# MEKA MULAN HOMER
#clf = Meka(
#        meka_classifier = 'meka.classifiers.multilabel.MULAN -S BPMLL',
#        weka_classifier = "weka.classifiers.trees.J48",
#        meka_classpath = mekaPath,
#        java_command = javaPath)



#clf = adaptation.BRkNNbClassifier(k=10)


baseClfTree = DecisionTreeClassifier()
baseClfSVM = SVC(kernel="rbf", gamma=0.1, C=10)


from skmultilearn.cluster import LabelCooccurrenceGraphBuilder, RandomLabelSpaceClusterer
from skmultilearn.ensemble import LabelSpacePartitioningClassifier
from skmultilearn.problem_transform import ClassifierChain
from sklearn.naive_bayes import GaussianNB

#clusterer = RandomLabelSpaceClusterer(cluster_size=10, cluster_count=5, allow_overlap=True)
#clf = ens.RakelO(base_classifier=baseClfTree, model_count=int(2*np.abs(targetIndex)), labelset_size=3, base_classifier_require_dense=True)
#clf = ens.RakelD(base_classifier=baseClfTree, labelset_size=3, base_classifier_require_dense=False)
#clf = ens.MajorityVotingClassifier(classifier=baseClfTree, clusterer=clusterer)
