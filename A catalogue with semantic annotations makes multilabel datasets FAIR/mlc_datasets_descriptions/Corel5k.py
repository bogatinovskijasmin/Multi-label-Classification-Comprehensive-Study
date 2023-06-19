from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Corel5k"

d["name"] = dataSetName
d["description"] = "Corel5k is a dataset from the multimedia domain. " \
                   "The samples represent Corel images. " \
                   "Each image is segmented using the Normalized Cuts method. " \
                   "The segments are then clustered into regions and described with 33 features each. " \
                   "For each image, there are 5-10 regions describing them. " \
                   "The features represent whether the region is present or not in a particular image. " \
                   "The labels are word description of the region. "



d["sameAs"] = ["https://cometa.ujaen.es/datasets/corel5k", "http://www.uco.es/kdis/mllresources/#Corel5kDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://link.springer.com/chapter/10.1007/3-540-47979-1_7", "doi.org/10.1007/3-540-47979-1_7"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Pinar Duygulu Sahin"
dd2["url"] = "https://scholar.google.com/citations?user=1KEMrHkAAAAJ&hl=en"

dd3["name"] = "David Forsyth"
dd3["url"] = "https://scholar.google.com/citations?user=5H0arvkAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))