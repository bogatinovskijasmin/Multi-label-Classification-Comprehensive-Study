from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Bookmarks"

d["name"] = dataSetName
d["description"] = "This is a multi-label datasets consisting of bookmark entries from the Bibsonomy system. The bookmark files contain metadata for bookmark items like the URL of the web page, a description of the web page, etc." \
                   "The fetures are given in BoW format. The labels represent different tags relevant for a bookmark entry. "


d["sameAs"] = ["http://www.uco.es/kdis/mllresources/#BookmarksDesc", "https://cometa.ujaen.es/datasets/bookmarks", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://pdfs.semanticscholar.org/1570/99d6ffd3ffca8cfca7955aff7c5f1a979ac9.pdf?_ga=2.210622165.1352770161.1568634463-1967250438.1556735199"]
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