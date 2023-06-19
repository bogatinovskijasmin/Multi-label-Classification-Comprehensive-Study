from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "3_sources-intern"

d["name"] = dataSetName
d["description"] = "3_sources is a collection of 4 multi-label datasets. It is collected from 3 news sources: BBC, Reuteres and The Gurdian. In total there are 948 news articles covering 416 news stories. Some " \
                   "of the stories report on same issues. It is a dataset primarly constriucted for the problem of multi-view learning. The feature preprocessign includes" \
                   "stemming using Porter algorithm, stop-words removal and low term frequency filtering (count <3 )."\
                   "Each story is annotated with one or more of the six topical labels: business, entertainment, health, politics, sport, technology. "



d["sameAs"] = ["http://www.uco.es/kdis/mllresources/#3sourcesDesc", "http://mlg.ucd.ie/datasets/3sources.html"]
d["identifier"] = ["https://link.springer.com/content/pdf/10.1007/978-3-642-04180-8_45.pdf", "https://doi.org/10.1007/978-3-642-04180-8_45"]
d["keywords"] = ["multi-label classification"]

dd2["name"] = "Derek Greene"
dd2["url"] = "https://scholar.google.com/citations?user=htlibRwAAAAJ&hl=en"

dd3["name"] = "Padraig Cunningham"
dd3["url"] = "https://scholar.google.com/citations?user=NEP3RPYAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))