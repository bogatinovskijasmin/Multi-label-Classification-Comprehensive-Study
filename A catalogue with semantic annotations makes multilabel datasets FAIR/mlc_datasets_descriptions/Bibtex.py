from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Bibtex"

d["name"] = dataSetName
d["description"] = "Bibtex is a dataset from the text domain. " \
                   "It emerges from the social bookmarking and publication-sharing system Bibsonomy. " \
                   "The data is stored and organized in BibTeX entries. " \
                   "The labels represent the different tags a user can assign to their BibTeX submission to the system."



d["sameAs"] = ["https://cometa.ujaen.es/datasets/bibtex", "http://www.uco.es/kdis/mllresources/#BibtexDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://pdfs.semanticscholar.org/1570/99d6ffd3ffca8cfca7955aff7c5f1a979ac9.pdf", "10.1.1.183.2636"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Ioannis Katakis"
dd2["url"] = "http://www.katakis.eu/"

dd3["name"] = "Ioannis Vlahavas"
dd3["url"] = "https://scholar.google.com/citations?user=xHIjg7EAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))