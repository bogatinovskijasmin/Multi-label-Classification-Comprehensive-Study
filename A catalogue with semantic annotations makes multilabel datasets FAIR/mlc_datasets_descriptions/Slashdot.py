from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Slashdot"

d["name"] = dataSetName
d["description"] = "Slashdot is a dataset that belong to text domain. " \
                   "It consists of BoW representation of articles obtained from the website $slashdot.org$. " \
                   "The labels represent different subject categories such as hardware, mobile, news, interviews, games etc."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/slashdot", "http://www.uco.es/kdis/mllresources/#SlashdotDesc"]
d["identifier"] = ["https://dl.acm.org/citation.cfm?id=2070629", "10.1007/s10994-011-5256-5"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "	Jesse Read"
dd2["url"] = "https://scholar.google.es/citations?user=4gNCRFAAAAAJ&hl=en"

dd3["name"] = "Eibe Frank"
dd3["url"] = "https://scholar.google.com/citations?user=dUV_NvIAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))