from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "scene"

d["name"] = dataSetName
d["description"] = "scene} is one of the most popular datasets from the multimedia domain, belonging to the subcategory of images. " \
                   "It provides a very intuitive way to depict the aim of MLC. " \
                   "The dataset is about the classification of different scenes on an image. " \
                   "There are a total of 6 labels beach, sunset, fall foliage, field, mountain and urban." \
                   " The images are described with 294 features derived from LUV space. "




d["sameAs"] = ["https://cometa.ujaen.es/datasets/scene", "http://www.uco.es/kdis/mllresources/#SceneDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://www.sciencedirect.com/science/article/pii/S0031320304001074#!", "doi.org/10.1016/j.patcog.2004.03.009"]
d["keywords"] = ["Image understanding", "Semantic scene classification", "Multi-label training", "Multi-label evaluation", "Image organization", "Cross-training", "Jaccard similarity"]

dd2["name"] = "Matthew Boutell"
dd2["url"] = "https://scholar.google.com/citations?user=LB5QBY4AAAAJ&hl=en"

dd3["name"] = "Christopher M Brown"
dd3["url"] = "https://scholar.google.com/citations?user=OaLLZy8AAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))