from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Delicious"

d["name"] = dataSetName
d["description"] = "Delicious  is a dataset from the text domain. " \
                   "The data is extracted from $del.icio.us$ social bookmarking site on the 1st of April 2007. " \
                   "It contains textual data of web pages alongside with their tags. " \
                   "The words appearing on the pages are given in a BoW representation. " \
                   "The labels represent the different tags that can appear on the bookmarking site."



d["sameAs"] = ["https://cometa.ujaen.es/datasets/delicious", "http://www.uco.es/kdis/mllresources/#DeliciousDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://www.researchgate.net/publication/228386519_Effective_and_efficient_multilabel_classification_in_domains_with_large_number_of_labels"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Grigorios Tsoumakas"
dd2["url"] = "https://scholar.google.si/citations?user=PlGKUhwAAAAJ&hl=en&oi=ao"

dd3["name"] = "Ioannis Vlahavas"
dd3["url"] = "https://scholar.google.com/citations?user=xHIjg7EAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))