from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "RCV1"

d["name"] = dataSetName
d["description"] = "RCV1 is a multi-label dataset from the text domain. The features are given in TD-IDF weighthin schema. The output labels can be organized into hierarchy. There are 5 versions of this dataset."


d["sameAs"] = ["http://www.uco.es/kdis/mllresources/#rcv1", "https://cometa.ujaen.es/datasets/rcv1sub1"]
d["identifier"] = ["https://dl.acm.org/citation.cfm?id=1005345" ]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "David D. Lewis"
dd2["url"] = "https://scholar.google.com/citations?user=f0oxRwsAAAAJ&hl=en"

dd3["name"] = "Fan Li"
dd3["url"] = "https://dl.acm.org/author_page.cfm?id=81372592748&coll=DL&dl=ACM&trk=0"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))