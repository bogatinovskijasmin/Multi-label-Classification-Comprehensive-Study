from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Flags"

d["name"] = dataSetName
d["description"] = "Flags is a dataset that contains information about countries flags. " \
                   "Its features describe the presence or absence of different symbols appearing on flags, " \
                   "such as triangles, information about population, language, religion etc. " \
                   "The labels represent the 7 colours: red, green, blue, yellow, white, black, orange that appear on flags."



d["sameAs"] = ["https://cometa.ujaen.es/datasets/flags", "http://www.uco.es/kdis/mllresources/#SrivastavaEtAl2005", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://www.researchgate.net/profile/Eduardo_Goncalves17/publication/262323962_A_Genetic_Algorithm_for_Optimizing_the_Label_Ordering_in_Multi-label_Classifier_Chains/links/570b91f608aed09e91750ec3.pdf", "10.1109/ICTAI.2013.76"]
d["keywords"] = ["multi-label classification", "classifier chains", "genetic algorithm"]

dd2["name"] = "Eduardo Corrêa Gonçalves"
dd2["url"] = "https://scholar.google.com.br/citations?user=cpxCM7QAAAAJ&hl=pt-BR"

dd3["name"] = "Freitas, Alex A."
dd3["url"] = "https://scholar.google.com/citations?user=NEP3RPYAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))