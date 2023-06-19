from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "ABPM"

d["name"] = dataSetName
d["description"] = "ABPM is a dataset with 33 features and 6 labels. " \
                   "The dataset has 270 records of blood pressure measurements from patients in a duration of 24 hours. " \
                   "The features represent general information for the patients as gender, age, weight, height, " \
                   "but also various statistical features obtained from the diastolic and systolic load values. " \
                   "The labels represent the presence and absence of validity, morning surge, blood pressure load, blood pressure variability, " \
                   "pulse pressure and circadian rhythm."



d["sameAs"] = ["https://data.mendeley.com/datasets/y4dh3b3tfx/1"]
d["identifier"] = ["https://data.mendeley.com/datasets/y4dh3b3tfx/1", "10.17632/y4dh3b3tfx.1"]
d["keywords"] = ["Amboulutray Blood Preassure"]

dd2["name"] = "Khalida Douibi"
dd2["url"] = "https://www.mendeley.com/profiles/khalida-douibi/"

dd3["name"] = "Mohammed Amine Chikh"
dd3["url"] = "https://scholar.google.com/citations?user=YZF0Gj0AAAAJ&hl=fr"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))