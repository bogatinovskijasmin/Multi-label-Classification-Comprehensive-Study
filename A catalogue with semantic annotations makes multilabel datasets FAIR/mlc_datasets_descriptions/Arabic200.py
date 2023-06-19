from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Arabic200"

d["name"] = dataSetName
d["description"] = "Arabic200 is a dataset obtained from Russia Today in Arabic news portal. " \
                   "It consists of news articles distributed in 40 categories. The features are numeric. " \
                   "There are multiple variants of the dataset available with 200, 500, 1000, 2000, 3000, 4000 features. " \
                   "The variant with 200 features is used in the experiments. "




d["sameAs"] = ["https://data.mendeley.com/datasets/322pzsdxwy/1"]
d["identifier"] = ["https://data.mendeley.com/datasets/322pzsdxwy/1", "10.17632/322pzsdxwy.1"]
d["keywords"] = ["Machine Learning", "Classification System", "Categorization", "Text Processing"]

dd2["name"] = "Bassam Al-Salemi"
dd2["url"] = "https://scholar.google.com/citations?user=M2l79b4AAAAJ&hl=en"

dd3["name"] = "Shahrul Azman Mohd Noah"
dd3["url"] = "https://scholar.google.com/citations?user=z00DOrYAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))