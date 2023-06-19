from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Ng20"

d["name"] = dataSetName
d["description"] = "Ng20 is a dataset containing news data. " \
                   "The features are given in a BoW representation." \
                   " The labels represent different topics such as politics, cars, religion, space etc."



d["sameAs"] = ["https://cometa.ujaen.es/datasets/ng20", "http://www.uco.es/kdis/mllresources/#20NGDesc"]
d["identifier"] = ["https://www.sciencedirect.com/science/article/pii/B9781558603776500487", "10.1016/B978-1-55860-377-6.50048-7"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Ken Lang"
dd2["url"] = "http://www.cs.cmu.edu/Groups/ml/ml.html"

d["creator"] = [dd2]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))