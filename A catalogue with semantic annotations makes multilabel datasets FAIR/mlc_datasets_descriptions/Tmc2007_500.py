from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Tmc2007 500"

d["name"] = dataSetName
d["description"] = "Tmc2007 500  is a dataset containing Aviation Safety Reporting textual data." \
                   " The texts are free text reports, obtained by crew members about various events during a flight." \
                   " The features are given in a BoW form. This version of the dataset has reduced description space from 49060 to 500." \
                   "The labels represent the various events that may occur during the flight."



d["sameAs"] = ["https://cometa.ujaen.es/datasets/tmc2007_500", "http://www.uco.es/kdis/mllresources/#StackexDesc"]
d["identifier"] = ["https://ieeexplore.ieee.org/document/1559692", "10.1109/AERO.2005.1559692"]
d["keywords"] = ["Data mining", "Information analysis", "Aerospace testing", "Text mining", "Functional analysis", "Data analysis", "Sensor systems", "Thermal sensors", "Manufacturing processes"]

dd2["name"] = "Ashok K. Srivastava"
dd2["url"] = "https://scholar.google.si/citations?user=m7uS4PcAAAAJ&hl=en&oi=ao"

dd3["name"] = "B. Zane-Ulman"
dd3["url"] = "https://ieeexplore.ieee.org/author/38270603300"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))