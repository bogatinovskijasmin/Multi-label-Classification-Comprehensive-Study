from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Emotions"

d["name"] = dataSetName
d["description"] = "Emotions is a dataset from the multimedia domain. " \
                   "It describes the relationship between music and emotions based on the Tellegen-Watson-Clarks model of mood. " \
                   "The obtained sound signals are used to calculate temporal and timber features. " \
                   "The labels represent 6 main emotions a music piece provides: amazed-surprised, happy-pleased, relaxing-calm, quite-still, sad-lonely, and angry-fearful. "



d["sameAs"] = ["https://cometa.ujaen.es/datasets/emotions", "http://www.uco.es/kdis/mllresources/#EmotionsDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://link.springer.com/chapter/10.1007/3-540-33521-8_30", "https://doi.org/10.1007/3-540-33521-8_30"]
d["keywords"] = ["Audio Data",  "Music Information Retrieval", "Audio Sample Musical", "Recording Ontology Graph"]

dd2["name"] = "Alicja Wieczorkowska"
dd2["url"] = "https://www.researchgate.net/profile/Alicja_Wieczorkowska"

dd3["name"] = "Zbigniew W. Ras"
dd3["url"] = "https://scholar.google.com/citations?user=2ihGAJkAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))