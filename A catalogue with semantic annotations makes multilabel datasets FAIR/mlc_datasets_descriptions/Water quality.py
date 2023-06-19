from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Water quality"

d["name"] = dataSetName
d["description"] = "Water Quality is dataset containing descriptions about the biological properties of a river. " \
                   "The features represent the different concentration of chemical components, such as biological oxygen demand, " \
                   "electrical conductivity, chemical oxygen demand, concentrations of different elements and compounds, water temperature and total hardness. " \
                   "The labels are represented by 14 taxa present at the sampling sites and their density. This dataset belongs to the domain of chemistry."



d["sameAs"] = ["http://www.uco.es/kdis/mllresources/#WaterQualityDesc"]
d["identifier"] = ["https://link.springer.com/chapter/10.1007/978-3-540-48247-5_4", "10.1007/978-3-540-48247-5_4"]
d["keywords"] = ["Chemical Oxygen Demand", "Biological Oxygen Demand", "River Water Quality", "Inductive Logic Programming", "Inductive Logic Programming System"]

dd2["name"] = "Hendrik Blockeel"
dd2["url"] = "https://scholar.google.com/citations?user=Eq5sUNpp0gwC&hl=en"

dd3["name"] = "Saso Dzeroski"
dd3["url"] = "https://scholar.google.com/citations?user=_aIV-aEAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))