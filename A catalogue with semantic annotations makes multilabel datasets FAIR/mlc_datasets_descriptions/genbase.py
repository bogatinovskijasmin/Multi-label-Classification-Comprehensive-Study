from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "genbase"

d["name"] = dataSetName
d["description"] = "Genbase is a dataset that contains protein sequences and its functional family labels. " \
                   "Since a protein sequence can have multiple functions the problem can be defined as a MLC task. " \
                   "Each protein sequence is mapped to an attribute vector. " \
                   "Since each protein sequence contains some motifs thus it can be represented as a " \
                   "set of 1's and 0's depending on the presence or absence of the motif in the sequence. " \
                   "The labels are grouped in the 10 most common families. " \
                   " The labels are the classes: oxidoreductases, isomerases, cytokines and growth factors, structural proteins, " \
                   "receptors, DNA or RNA associated proteins, transferals, protein secretion and chaperoned, hydrolysis. " \
                   "GenMiner is used as a tool to prepare the data. "




d["sameAs"] = ["https://cometa.ujaen.es/datasets/genbase", "http://www.uco.es/kdis/mllresources/#GenbaseDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://link.springer.com/chapter/10.1007/11573036_42", "10.1007/11573036_42"]
d["keywords"] = ["Classification Algorithm", "Weight Vote", "Sequential Minimal Optimization", "Classifier Selection", "Protein Classification"]

dd2["name"] = "Douglas Turnbull"
dd2["url"] = "https://scholar.google.com/citations?user=CaEaSR8AAAAJ&hl=en"

dd3["name"] = "Gert Lanckriet"
dd3["url"] = "https://scholar.google.com/citations?user=acmtRMAAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))