from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "IMDB"

d["name"] = dataSetName
d["description"] = "IMDB dataset is a multi-label dataset derived from a freely plot descriptions of movies. The labels represent the different geners a movie can be assigned to." \
                   "The features are BoW representation of the plot descriptions. "


d["sameAs"] = ["https://cometa.ujaen.es/datasets/imdb", "http://www.uco.es/kdis/mllresources/#ImdbDesc"]
d["identifier"] = ["https://link.springer.com/chapter/10.1007/978-3-642-04174-7_17", "10.1007/978-3-642-04174-7_17"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Jesse Read"
dd2["url"] = "https://scholar.google.es/citations?user=4gNCRFAAAAAJ&hl=en"

dd3["name"] = "Eibe Frank"
dd3["url"] = "https://scholar.google.com/citations?user=dUV_NvIAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))