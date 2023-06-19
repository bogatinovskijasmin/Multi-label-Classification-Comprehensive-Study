from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Enron"

d["name"] = dataSetName
d["description"] = "Enron is a dataset containing e-mail messages from the Enron corpus. It belongs to the group of text domain. " \
                   "The features are represented in BoW format. " \
                   "The targets represent different topics being considered. " \
                   "For example company strategy, legal advice, humour etc."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/slashdot", "http://www.uco.es/kdis/mllresources/#SlashdotDesc"]
d["identifier"] = ["http://nl.ijs.si/janes/wp-content/uploads/2014/09/klimtyang04b.pdf", "10.1007/978-3-540-30115-8_22"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Bryan Klimt"
dd2["url"] = "https://www.semanticscholar.org/author/Bryan-Klimt/1946210"

dd3["name"] = "Yiming Yang"
dd3["url"] = "https://scholar.google.com/citations?user=MlZq4XwAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))