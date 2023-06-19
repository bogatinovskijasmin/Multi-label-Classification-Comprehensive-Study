from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "birds"

d["name"] = dataSetName
d["description"] = "Birds is a dataset representing the problem of bird species classification from acoustic recordings. " \
                   "In one recording multiple species may appear. " \
                   "After obtaining the raw audio signals, the signals are filtered and segmented. " \
                   "From each of the segments, various features from time and frequency domain are extracted. " \
                   "The labels represent if a type of bird is present in the particular instance. " \
                   "It belongs to the multimedia domain in the subcategory audio."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/birds", "http://www.uco.es/kdis/mllresources/#BirdsDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://www.ncbi.nlm.nih.gov/pubmed/22712937", "10.1121/1.4707424"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Forrest Briggs"
dd2["url"] = "https://scholar.google.com/citations?user=WmyVSLQAAAAJ&hl=en"

dd3["name"] = "Xiaoli Z. Fern"
dd3["url"] = "https://www.researchgate.net/profile/Xiaoli_Fern"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))