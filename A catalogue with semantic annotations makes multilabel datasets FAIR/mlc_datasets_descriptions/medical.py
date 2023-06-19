from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "medical"

d["name"] = dataSetName
d["description"] = "Medical is a dataset composed of medical records, thus belongs to the group of text domain. " \
                   "The features are BoW representation of the datasets. " \
                   "The labels represent 45 possible tag disease."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/medical", "http://www.uco.es/kdis/mllresources/#MedicalDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://www.aclweb.org/anthology/W07-1017"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Koby Crammer"
dd2["url"] = "https://scholar.google.com/citations?user=NQgRwKAAAAAJ&hl=zh-CN"

dd3["name"] = "Partha Pratim Talukdar"
dd3["url"] = "https://scholar.google.com/citations?user=CIZwXAcAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))