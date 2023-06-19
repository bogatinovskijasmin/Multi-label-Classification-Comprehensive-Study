from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Stackex chemistry"

d["name"] = dataSetName
d["description"] = "Stackex chemistry is a dataset that originate from one of the 6 stackex different forums. " \
                   "In this study the forums of computer science, chess and philosophy are used. " \
                   "The features are given in term-frequency of the words per forum post. " \
                   "These datasets belong to text domain. " \
                   "The labels represent the different topics related to the posts." \
                   "The datasets are independent among different forums."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/stackex_chemistry", "http://www.uco.es/kdis/mllresources/#StackexDesc"]
d["identifier"] = ["https://ieeexplore.ieee.org/document/7313677", " 10.1109/EUROCON.2015.7313677"]
d["keywords"] = ["Machine Learning", "Multi-label classification"]

dd2["name"] = "Francisco Charte"
dd2["url"] = "https://scholar.google.com/citations?user=i8l_80EAAAAJ&hl=en"

dd3["name"] = "Francisco Herrera"
dd3["url"] = "https://scholar.google.com/citations?user=HULIk-QAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))