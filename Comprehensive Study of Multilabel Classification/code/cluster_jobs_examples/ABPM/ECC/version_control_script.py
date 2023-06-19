import pandas as pd
import numpy as np
import scipy as sp
import arff
import os
import pickle
import random
import sys
import json
import time
import shutil

# utils
from scipy import sparse
from time import time

from skmultilearn.ext.meka import SUPPORTED_VERSION
from skmultilearn.ext import download_meka
from skmultilearn import ext
from skmultilearn import adapt as adaptation

### USED MEASURES FOR EVALUATION

from sklearn.metrics import label_ranking_loss
from sklearn.metrics import label_ranking_average_precision_score
from sklearn.metrics import coverage_error               # this error has different implementation

from sklearn.metrics import average_precision_score      # used to calculate APRC  score
from sklearn.metrics import roc_auc_score                # used to calculate AUROC score

from sklearn.metrics import hamming_loss                 # hamming loss
from sklearn.metrics import precision_score              # use average = 'samples"
from sklearn.metrics import recall_score                 # use average = 'samples"
from sklearn.metrics import f1_score                     # use average = 'samples"
from sklearn.metrics import jaccard_similarity_score     # accuracy
from sklearn.metrics import accuracy_score               # in multi-label setting this represents 0/1 subset accuracy


# Label-based metrics x2  micro and macro
from sklearn.metrics import precision_score              # average = 'micro" & 'macro'
from sklearn.metrics import recall_score                 # average = 'micro" & 'macro'
from sklearn.metrics import f1_score                     # average = 'micro" & 'macro'


"""
This script contains summary of the libraries used in the work.
Moreover, it contains the global variables defined across the scripts and the imported libraries that are required.

Note: Be careful of not interfering with the global names. Use them smartly.
"""


mekaPath = ext.download_meka()                                                       # contains the pat of meka.jar executable
javaPath = "/usr/bin/java"                                                           # contains the path of java.jar executable
setSeed = 2                                                                          # contains the seed to be used accross libraires
dataSetsPath = '/media/jasminb/ubuntu_data/Multi_label_learning/ProcessedDatasets/'  # contains the path to the stored datasets


random.seed = setSeed
np.random.seed(setSeed)

print("Pandas version: ", pd.__version__)
print("Numpy version: ", np.__version__)
print("Scipy version: ", sp.__version__)
print("Arff version: ", arff.__version__)
print("Skmultilearn version: 0.2.0")