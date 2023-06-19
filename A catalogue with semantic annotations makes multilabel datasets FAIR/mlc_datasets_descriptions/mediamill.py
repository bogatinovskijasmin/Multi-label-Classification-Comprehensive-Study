from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "mediamill"

d["name"] = dataSetName
d["description"] = "Mediamill dataset for generic video indexing, which was extracted tom the TRECVID 2005/2006 benchmark. It belongs to the multimedia domain." \
                   "The training dataset contains 85 hours of international broadcast news data categorized into " \
                   "101 labels and each video instance is represented as a 120-dimensional feature vector of numeric features."


d["sameAs"] = ["https://cometa.ujaen.es/datasets/mediamill", "http://www.uco.es/kdis/mllresources/#MediamillDesc"]
d["identifier"] = ["https://www.researchgate.net/publication/221572843_The_challenge_problem_for_automated_detection_of_101_semantic_concepts_in_multimedia", "10.1145/1180639.1180727" ]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Cees G. M. Snoek"
dd2["url"] = "https://scholar.google.com/citations?user=0uKdbscAAAAJ&hl=en"

dd3["name"] = "Jan-Mark Geusebroek"
dd3["url"] = "https://scholar.google.com/citations?user=1elNDpMAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))