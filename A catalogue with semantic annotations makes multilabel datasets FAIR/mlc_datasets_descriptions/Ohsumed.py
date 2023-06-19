from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Ohsumed"

d["name"] = dataSetName
d["description"] = "Ohsumed  is a dataset from text domain. " \
                   "It is a subset from the MEDLINE database, which is a bibliographic database of peer-reviews of medical literature. " \
                   "The features are BoW representation of the words appearing in the reports. " \
                   "The labels represent 23 medical categories of cardiovascular disease. "



d["sameAs"] = ["https://cometa.ujaen.es/datasets/ohsumed", "http://www.uco.es/kdis/mllresources/#OhsumedDesc"]
d["identifier"] = ["https://link.springer.com/chapter/10.1007/BFb0026683", "10.1007/BFb0026683"]
d["keywords"] = ["Support Vector Machine",  "Radial Basic Function", "Text Categorization",  "Irrelevant Feature",  "Linear Threshold Function"]

dd2["name"] = "Throsten Joachims"
dd2["url"] = "https://scholar.google.com/citations?user=5tk1PV8AAAAJ&hl=en"

d["creator"] = [dd2]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))