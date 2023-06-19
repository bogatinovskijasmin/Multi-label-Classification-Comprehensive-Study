from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Proteins virus"

d["name"] = dataSetName
d["description"] = "Proteins datasets are set of 3 datasets from the area of bioinformatics. " \
                   "They describe the problem of sub-cellular localization. " \
                   "As input are taken the sequence descriptors of the proteins for  humans, virus, plant. " \
                   "The calculation of the features is done with the \"propy\" library." \
                   " The library takes as input the protein sequences and uses the default " \
                   "settings of the methods used to extract the features. " \
                   "The features describe structural and physio-chemical properties of the proteins and " \
                   "some of them include amino acid compositions, dipeptide compositions, transition, " \
                   "Moran auto-correlation, distributions, sequence-order-coupling numbers etc."




d["sameAs"] = ["http://www.csbio.sjtu.edu.cn/bioinf/Hum-mPLoc3/"]
d["identifier"] = ["https://www.ncbi.nlm.nih.gov/pubmed/27993784", " 10.1093/bioinformatics/btw723"]
d["keywords"] = ["Machine Learning", "Multi-label classification"]

dd2["name"] = "Hang Zhou"
dd2["url"] = "None"

dd3["name"] = "Hong-Bin Shen"
dd3["url"] = "https://dblp.org/pers/hd/s/Shen:Hong=Bin"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))