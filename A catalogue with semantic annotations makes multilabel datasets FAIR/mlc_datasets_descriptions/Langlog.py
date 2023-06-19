from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Longlog"

d["name"] = dataSetName
d["description"] = "Longlog  is a dataset from the text domain." \
                   " It consists of various topics relating to predominantly English language, " \
                   "obtained from Language Log Forum. " \
                   "The dataset is given in BoW format. " \
                   "There are 75 labels representing different aspects for the language, " \
                   "for example, punctuation, humour, errors, administration, negation etc."




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