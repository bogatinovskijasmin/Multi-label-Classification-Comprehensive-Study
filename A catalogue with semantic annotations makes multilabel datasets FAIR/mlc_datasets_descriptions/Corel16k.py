from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Corel16k010"

d["name"] = dataSetName
d["description"] = "Corel16k010 is a dataset from the multimedia domain. " \
                   "The samples represent Corel images. " \
                   "Each image is segmented using the Normalized Cuts method. Each image is represented with the 8 largest segments. " \
                   "The segments are then clustered into regions and described with 40 features each. " \
                   "The features represent visual properties such as size, position, color, texture and shape. " \
                   "The features represent whether the region is present or not in a particular image. " \
                   "The labels are word description of the region. "



d["sameAs"] = ["https://cometa.ujaen.es/datasets/corel16k010", "http://www.uco.es/kdis/mllresources/#Corel16kDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["http://www.jmlr.org/papers/volume3/barnard03a/barnard03a.pdf"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Barnard Kobus"
dd2["url"] = "https://scholar.google.com/citations?user=fKESO6sAAAAJ&hl=en"

dd3["name"] = "Jordan Michael"
dd3["url"] = "https://scholar.google.com/citations?user=yxUduqMAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))