from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Reuters k500"

d["name"] = dataSetName
d["description"] = "Reuters k500 is a dataset originate from Reuters RCV1 corpus. Since the RCV1 corpus posses around 46000 features, applying feature selection technique " \
                   "reduces the number of features to 500. The features are given in tf-idf format." \
                   "Since the labels in the corpus have a hierarchical structure in order to be used in the MLC setting the hierarchy is flattened."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/slashdot", "http://www.uco.es/kdis/mllresources/#SlashdotDesc"]
d["identifier"] = ["https://researchcommons.waikato.ac.nz/handle/10289/4645?show=full"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Read, Jesse"
dd2["url"] = "https://scholar.google.es/citations?user=4gNCRFAAAAAJ&hl=en"

#dd3["name"] = "Yiming Yang"
#dd3["url"] = "https://scholar.google.com/citations?user=MlZq4XwAAAAJ&hl=en"

d["creator"] = [dd2]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))