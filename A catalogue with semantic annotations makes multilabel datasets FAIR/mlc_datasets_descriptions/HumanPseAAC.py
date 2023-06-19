from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "GnegativePseAAC"

d["name"] = dataSetName
d["description"] = "GnegativePseAAC is a dataset from the area of bioinformatics.  It describes the task of predicting sub-cellular locations of proteins in " \
                   "organism according to their sequences. However, compared to GO datasets it represents the protein samples using pseudo amino acid composition including 20 amino-acid, " \
                   "20 pseudo-amino acid and 400 dipeptide components. " \
                   "The labels are the subcellular locations where a protein may appear. These numbers are different depending on the organism at interest."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/HumanGO", "http://www.uco.es/kdis/mllresources/#HumanDesc"]
d["identifier"] = ["https://doi.org/10.1016/j.knosys.2016.01.032", "https://www.sciencedirect.com/science/article/pii/S0950705116000526"]
d["keywords"] = ["Multi-label classification", "Dimensionality reduction", "Feature extraction", "Principal component analysis", "Hilbert–Schmidt independence criterion",
                 "Eigenvalue problem"]

dd2["name"] = "Jianhua Xu"
dd2["url"] = "https://www.mendeley.com/authors/57194768618/"

dd3["name"] = "Chengyu Sun"
dd3["url"] = "https://www.mendeley.com/authors/57113934100/"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))