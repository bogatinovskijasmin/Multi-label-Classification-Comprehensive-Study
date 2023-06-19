from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "yeast"

d["name"] = dataSetName
d["description"] = "Yeast is a dataset from the domain of biology. " \
                   "The data represent micro-array expressions and phylogeny profiles of genes. " \
                   "The labels can be multiple of the following functional groups: metabolism, energy, transcription, protein synthesis, " \
                   "protein destination, cell growth, transport facilitation, cell transport, cellular biogenesis, ionic homeostasis, cellular organization, transportable elements, cell death and ageing and cell communication. " \
                   "So, the task is to predict the function of a gene using its micro-array expression."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/HumanGO", "http://www.uco.es/kdis/mllresources/#YeastDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://pdfs.semanticscholar.org/af95/a95febc76243b521b4559edf87670d513a7a.pdf?_ga=2.112505414.397912381.1566305008-1967250438.1556735199"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Andre Elisseeff a"
dd2["url"] = "https://www.semanticscholar.org/author/Andr%C3%A9-Elisseeff/1766703"

dd3["name"] = "Jason Weston"
dd3["url"] = "https://scholar.google.com/citations?user=lMkTx0EAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))