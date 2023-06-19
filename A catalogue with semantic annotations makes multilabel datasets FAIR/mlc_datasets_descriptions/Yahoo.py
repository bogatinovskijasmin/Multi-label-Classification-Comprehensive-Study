from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Yahoo"

d["name"] = dataSetName
d["description"] = "Yahoo is a multi-label dataset from the text domain. The text is from Web pages linked from the yahoo.com domain. The features are given in BoW format. The labels represent different subcategories relevant for the topic. There are 11 categories for this collection including: arts, buisiness, computer, education, entertainment, health, recreation, reference, science, social and society."


d["sameAs"] = ["https://cometa.ujaen.es/datasets/yahoo_arts", "http://www.uco.es/kdis/mllresources/#YahooDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.67.5909&rep=rep1&type=pdf", "10.1.1.67.5909" ]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Naonori Ueda"
dd2["url"] = "https://scholar.google.co.jp/citations?user=lelCr80AAAAJ&hl=en"

dd3["name"] = "Kazumi Saito"
dd3["url"] = "https://www.semanticscholar.org/author/Kazumi-Saito/1727070"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))