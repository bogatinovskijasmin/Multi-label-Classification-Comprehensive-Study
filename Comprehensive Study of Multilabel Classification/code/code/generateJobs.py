from version_control_script import *
from dataSetsPreprocessing import *
from algorithmConfiguration import *
"""
Input: 
      input1: File containing the properties of the algorithms. 
      input2: File containing the configuration of the algorithms.
      
This script generates the jobs to run on cluster.
Each job has a python script inside it that requires 2 arguments.
The first argument is the name of the dataset.
The second argument is the name of the algorithm and its configuration.
The second argument has an overhead in terms of FLAG. This FLAG is used to instantiate the part of the code that should be used.

Output: Folders containg the needed configuration for the runs.
"""
#dataSetsPath = '/media/jasminb/ubuntu_data/Multi_label_learning/ProcessedDatasets/'
#dataSet = '/media/jasminb/ubuntu_data/Multi_label_learning/ProcessedDatasetsFolds/'
#dataSetsNames = os.listdir(dataSet)
methods = ["MLTSVM", "RAkEL1", "RAkEL2", "LINE", "RSMLCC", "RSMLLC", "CLR", "EBR", "ECC", "ELP", "EPS", "PSt", "BPNN", "HOMER", "CDN", "MBR", "BR", "MLkNN", "CLEMS", "MLARM", "BRkNN", "SSM", "LP", "CC"]

#methods  = ["HOMER"]




batch0 = ["flags", "ABPM", "foodtruck", "CHD_49",  "Water_quality", "emotions", "Virus_PseAAC", "VirusGO", "GpositivePseAAC"]
batch1 = ["GpositiveGO", "3sources_guardian1000", "3sources_bbc1000", "proteins_virus", "3sources_intern3000", "yeast", "birds", "scene"]
batch2 = ["GnegativePseACC", "PlantPseAAC", "cal500", "proteins_plant", "GnegativeGO", "HumanPseAAC", "genbase", "Yelp", "PlantGO"]
batch3 = ["proteins_human", "medical", "slashdot", "langlog", "stackex_chess",  "reutersk500", "tmc2007_500"]

batch4 = ["twitterEmotions", "ohsumed", "ng20", "HumanGO", "Arabic500", "mediamill", "stackex_chess", "enron",  "stackex_philosophy", ]

sepBatch = ["stackex_cs", "bibtex", "stackex_cooking", "delicious", "corel16k001", "imdb"]



batch5 = ["corel5k", "corel16k001", "corel16k002", "corel16k003", "corel16k004", "corel16k005", "corel16k006", "corel16k007"]

batch6 = ["Arabic2000", "Arabic3000", "Arabic4000", "Arabic1000" ]
batch7 = [ "corel16k008", "corel16k009", "corel16k010", "yahoo_arts", "yahoo_business", "yahoo_health", "yahoo_entertainment", "yahoo_recreation", "yahoo_science"]
batch8 = ["yahoo_reference", "yahoo_education", "yahoo_social", "yahoo_society", "yahoo_computer", "eurloexsm"]

batch9 = ["rcv1sub1", "rcv1sub2", "rcv1sub3", "rcv1sub4", "rcv1sub5"]
batch10 = ["tmc2007", "bookmarks", "eurlexdc", "eurloexsm"]

sepBatch1 = ["corel5k", "rcv1sub1", "yahoo_arts", "yahoo_education", "yahoo_computer", "bookmarks"]

#methods = ["CLEMS"]
dataSetsNames = ["3sources_bbc1000", "3sources_guardian1000", "3sources_intern3000", "ML_20geners", "ML_SPIRIT"]

#methods = ["RSMLCC", "ELP", "BPNN", "PSt"]
#methods = ["RAkEL1", "RAkEL2", "RSMLLC", "RSMLCC", "HOMER", "ECC", "ELP"]

for dataset in dataSetsNames:
    try:
        destination = "/media/jasminb/ubuntu_data/Cluster/batchNew/"

        os.mkdir(destination + dataset)
        for method in methods:
            try:
                os.mkdir(destination + "/" + dataset + "/" + method)
                with open(destination + "/" + dataset + "/" + method + "/" + method + "execution.sh", "w") as sh_file:
                    content = []
                    content.append("tar xvzf scikit_ml_learn_data.tar.gz\n")
                    content.append("python3 execution_script.py" + " " + dataset + " " + method + " " + "val\n")
                    content.append("python3 parseJsonFiles.py"  + " " + dataset + " " + method + " \n")
                    content.append("tar -czf results_" + dataset + "_" + method + ".tar.gz *\n")
                    sh_file.writelines(content)
                with open(destination + "/" + dataset + "/" + method + "/method.xrsl", "w") as xrsl:
                    content1 = []
                    content1.append("&\n")
                    content1.append("(executable=\"" + method+"execution.sh\")\n")
                    content1.append("(jobname=\"" + dataset + "_" + method + "\")\n")
                    content1.append("(stdout = \"" + dataset + "_" + method + ".log\")\n")
                    content1.append("(join = yes)\n")
                    content1.append("(walltime = \"24 hours\")\n")
                    content1.append("(gmlog = \"log\")\n")
                    content1.append("(memory = \"5000\")\n")
                    content1.append("(count=\"2\")\n")
                    content1.append("(runtimeenvironment=APPS/BASE/XENIAL-E8)\n")
                    content1.append("(countpernode=\"2\")\n")
                    content1.append("(inputfiles = (\"algorithmConfiguration.py\" \"/home/jasminb/PycharmProjects/MasterThesis_/algorithmConfiguration.py\") \n"
                                    "              (\"evaluation_script.py\"  \"/home/jasminb/PycharmProjects/MasterThesis_/evaluation_script.py\") \n"
                                    "              (\"version_control_script.py\"  \"/home/jasminb/PycharmProjects/MasterThesis_/version_control_script.py\") \n"
                                    "              (\"execution_script.py\"  \"/home/jasminb/PycharmProjects/MasterThesis_/execution_script.py\") \n"
                                    "              (\"parseJsonFiles.py\"  \"/home/jasminb/PycharmProjects/MasterThesis_/parseJsonFiles.py\") \n"
                                    "              (\"" + dataset+"fold1.arff\""  + " " + "\"gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/" + dataset+"/"+dataset+"_folds/" + dataset+"fold1.arff\") \n"
                                    "              (\"" + dataset+"fold2.arff\""  + " " +  "\"gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/" + dataset+"/"+dataset+"_folds/" + dataset+"fold2.arff\") \n"                                                                                                                                                                                                                                       
                                    "              (\"" + dataset+"fold3.arff\""  + " " +  "\"gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/" + dataset+"/"+dataset+"_folds/" + dataset+"fold3.arff\") \n"
                                    "              (\"scikit_ml_learn_data.tar.gz\"  \"gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/scikit_ml_learn_data.tar.gz\") \n"
                                    "              (\"dataSetsPreprocessing.py\" \"/home/jasminb/PycharmProjects/MasterThesis_/dataSetsPreprocessing.py\"))\n")

                    content1.append("(outputfiles = (\"results_" + dataset + "_" + method + ".tar.gz\" \" \" ))\n")
                    #content1.append("(queue != \"gridgpu\")\n")
                    xrsl.writelines(content1)
            except:
                with open(destination + "/" + dataset + "/" + method + "/" + method + "execution.sh", "w") as sh_file:
                    content = []
                    content.append("tar xvzf scikit_ml_learn_data.tar.gz\n")
                    content.append("python3 execution_script.py" + " " + dataset + " " + method + " " + "val\n")
                    content.append("python3 parseJsonFiles.py"  + " " + dataset + " " + method + " \n")
                    content.append("tar -czf results_" + dataset + "_" + method + ".tar.gz *\n")
                    sh_file.writelines(content)
                with open(destination + "/" + dataset + "/" + method + "/method.xrsl", "w") as xrsl:
                    content1 = []
                    content1.append("&\n")
                    content1.append("(executable=\"" + method+"execution.sh\")\n")
                    content1.append("(jobname=\"" + dataset + "_" + method + "\")\n")
                    content1.append("(stdout = \"" + dataset + "_" + method + ".log\")\n")
                    content1.append("(join = yes)\n")
                    content1.append("(walltime = \"24 hours\")\n")
                    content1.append("(gmlog = \"log\")\n")
                    content1.append("(memory = \"5000\")\n")
                    content1.append("(count=\"2\")\n")
                    content1.append("(runtimeenvironment=APPS/BASE/XENIAL-E8)\n")
                    content1.append("(countpernode=\"2\")\n")
                    content1.append("(inputfiles = (\"algorithmConfiguration.py\" \"/home/jasminb/PycharmProjects/MasterThesis_/algorithmConfiguration.py\") \n"
                                    "              (\"evaluation_script.py\"  \"/home/jasminb/PycharmProjects/MasterThesis_/evaluation_script.py\") \n"
                                    "              (\"version_control_script.py\"  \"/home/jasminb/PycharmProjects/MasterThesis_/version_control_script.py\") \n"
                                    "              (\"execution_script.py\"  \"/home/jasminb/PycharmProjects/MasterThesis_/execution_script.py\") \n"
                                    "              (\"parseJsonFiles.py\"  \"/home/jasminb/PycharmProjects/MasterThesis_/parseJsonFiles.py\") \n"
                                    "              (\"" + dataset+"fold1.arff\""  + " " + "\"gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/" + dataset+"/"+dataset+"_folds/" + dataset+"fold1.arff\") \n"
                                    "              (\""+ dataset+"fold2.arff\""  + " " +  "\"gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/" + dataset+"/"+dataset+"_folds/" + dataset+"fold2.arff\") \n"                                                                                                                                                                                                                                       
                                    "              (\"" + dataset+"fold3.arff\""  + " " +  "\"gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/" + dataset+"/"+dataset+"_folds/" + dataset+"fold3.arff\") \n"
                                    "              (\"scikit_ml_learn_data.tar.gz\"  \"gsiftp://dcache.arnes.si/data/arnes.si/gen.vo.sling.si/jasminb/folds/scikit_ml_learn_data.tar.gz\") \n"
                                    "              (\"dataSetsPreprocessing.py\" \"/home/jasminb/PycharmProjects/MasterThesis_/dataSetsPreprocessing.py\"))\n")



                    content1.append("(outputfiles = (\"results_" + dataset +"_" + method + ".tar.gz\" \" \" ))\n")
                    #content1.append("(queue != \"gridgpu\")\n")
                    xrsl.writelines(content1)
            #print("stignav TUKA")
            #shutil.copy2("dataSetsPreprocessing.py", destination + "/" + dataset + "/" + method)
            #shutil.copy2("algorithmConfiguration.py", destination + "/" + dataset + "/" + method)
            #shutil.copy2("evaluation_script.py", destination + "/" + dataset + "/" + method)
            #shutil.copy2("version_control_script.py", destination + "/" + dataset + "/" + method)
            #shutil.copy2("execution_script.py", destination + "/" + dataset + "/" + method)
            #shutil.copy2("parseJsonFiles.py", destination + "/" + dataset + "/" + method)
            #shutil.copy2("scikit_ml_learn_data.tar.gz", destination + "/" + dataset + "/" + method)
            #shutil.copy2("xenial64JB.sif", destination + "/" + dataset + "/" + method)
            os.makedirs(destination + "/" + dataset + "/" + method + "/" + placeData + dataset + "/" + dataset + "_folds/")
            #copy_tree(dataSet + "/" + dataset, destination + "/" + dataset + "/" + method + placeData + dataset)

    except:
           print("Duplicate")

