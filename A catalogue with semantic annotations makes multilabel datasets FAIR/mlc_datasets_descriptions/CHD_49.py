from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "CHD_49"

d["name"] = dataSetName
d["description"] = "CHD is a dataset from the medical domain. " \
                   "It describes the problem of diagnosing coronary heart disease via traditional Chinese medicine approaches. " \
                   "The features represent the presence or absence of different symptoms accessed via feelings of cold or warm, sweating, head, body, chest, urine etc. " \
                   "The labels represent the 6 commonly-used patterns, including deficiency of heart qi syndrome, deficiency of heart yang syndrome, " \
                   "deficiency of heart yin syndrome, qi stagnation syndrome, turbid phlegm syndrome, and blood stasis syndrome."



d["sameAs"] = ["http://www.uco.es/kdis/mllresources/#CHD49Desc"]
d["identifier"] = ["https://bmccomplementalternmed.biomedcentral.com/articles/10.1186/1472-6882-10-37", "10.1186/1472-6882-10-37"]
d["keywords"] = ["Coronary Heart Disease", "Traditional Chinese Medicine", "Test Instance", "Forecast Accuracy", "Forecast Result"]

dd2["name"] = "Guo-Ping Liu"
dd2["url"] = "https://www.ncbi.nlm.nih.gov/pubmed?cmd=search&term=Guo-Ping%20Liu"

dd3["name"] = "Yi-Qin Wang"
dd3["url"] = "https://www.researchgate.net/profile/Yi_Qin_Wang"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))