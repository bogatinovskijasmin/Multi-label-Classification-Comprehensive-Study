import pandas as pd
import numpy as np



targets = ['MLkNN', 'MLARM', 'DEEP1',
       'PCT', 'BPNN', 'RFPCT', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
       'BR', 'HOMER', 'Ada300', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
       'RFDTBR', 'TREMLCnew', 'MBR', 'CDN', 'ECCJ48', 'EBRJ48', 'SSM',
       'RSMLCC']

problem_transformation = ['EPS', 'CDE', 'LP', 'BR', 'HOMER', 'Ada300', 'RAkEL2', 'CC',
       'CLR', 'PSt', 'TREMLC', 'RFDTBR', 'TREMLCnew', 'MBR', 'CDN', 'ECCJ48',
       'EBRJ48', 'SSM', 'RSMLCC']

algortihm_adaptation = ['MLkNN', 'MLARM', 'DEEP1', 'PCT', 'BPNN', 'RFPCT', 'MLTSVM',
       'DEEP4', 'CLEMS']

ensembles = ['RFPCT', 'EPS', 'CDE', 'HOMER', 'Ada300', 'RAkEL2', 'CC', 'TREMLC', 'RFDTBR', 'TREMLCnew', 'MBR', 'CDN', 'ECCJ48', 'EBRJ48', 'SSM', 'RSMLCC']

br_vs_lp_single_to_drop = ['MLkNN', 'MLARM', 'DEEP1',
       'PCT', 'BPNN', 'RFPCT', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'HOMER', 'Ada300', 'RAkEL2', 'CC', 'TREMLC',
       'RFDTBR', 'TREMLCnew', 'MBR', 'CDN', 'ECCJ48', 'EBRJ48', 'SSM',
       'RSMLCC']

br_vs_lp = ["BR", "CLR"]

problem_transformation_ensembles_to_drop = ['MLkNN', 'MLARM', 'DEEP1', 'PCT', 'BPNN', 'MLTSVM', 'DEEP4', 'CLEMS', 'LP', 'BR', 'CLR', 'PSt']

def read_meta_dataset_for_measure(meta_dataset_path, measure):
    meta_dataset = pd.read_csv(meta_dataset_path+measure).iloc[:,1:]
    meta_features = meta_dataset.drop(['MLkNN', 'MLARM', 'DEEP1',
                       'PCT', 'BPNN', 'RFPCT', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
                       'BR', 'HOMER', 'Ada300', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
                       'RFDTBR', 'TREMLCnew', 'MBR', 'CDN', 'ECCJ48', 'EBRJ48', 'SSM',
                       'RSMLCC'], axis=1)

    meta_targets = meta_dataset.loc[:, ["index", 'MLkNN', 'MLARM', 'DEEP1',
                                        'PCT', 'BPNN', 'RFPCT', 'MLTSVM', 'DEEP4', 'CLEMS', 'EPS', 'CDE', 'LP',
                                        'BR', 'HOMER', 'Ada300', 'RAkEL2', 'CC', 'CLR', 'PSt', 'TREMLC',
                                        'RFDTBR', 'TREMLCnew', 'MBR', 'CDN', 'ECCJ48', 'EBRJ48', 'SSM',
                                        'RSMLCC']]

    return meta_features, meta_targets

def numeric_rise(meta_target):
    return np.max(meta_target.iloc[:, 1:].values, axis=1).tolist()

def numeric_down(meta_target):
    return np.min(meta_target.iloc[:, 1:].values, axis=1).tolist()

def meta_target_extract_larger_better(meta_target):
    pom = []
    ret = np.argmax(meta_target.iloc[:, 1:].values, axis=1).tolist()
    for x in ret:
        pom.append(meta_target.iloc[:, 1:].columns[x])
    print(pom)
    return pom

def meta_target_extract_smaller_better(meta_target):
    pom = []
    ret = np.argmax(meta_target.iloc[:, 1:].values, axis=1).tolist()
    for x in ret:
        pom.append(targets[x])
    return pom

def problem_transformation_vs_algortihm_adap(scenario1_targets):
    pom = []
    for x in scenario1_targets:
        if x in problem_transformation:
            pom.append(1)
        else:
            pom.append(0)
    return np.array(pom)

def ensemble_vs_single_target(scenario2_targets):
    pom = []
    for x in scenario2_targets:
        if x in ensembles:
            pom.append(1)
        else:
            pom.append(0)
    return np.array(pom)

def br_vs_lp_singletons(scenario3_targets):
    pom = []
    for x in scenario3_targets:
        if x in br_vs_lp:
            pom.append(1)
        else:
            pom.append(0)
    return np.array(pom)

def problem_transformation_binary_relevance_vs_label_powerset(meta_target):
    return meta_target.drop(br_vs_lp_single_to_drop,axis=1)


