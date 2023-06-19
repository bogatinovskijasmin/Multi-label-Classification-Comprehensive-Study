from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "cal500"

d["name"] = dataSetName
d["description"] = "Cal 500 is a dataset from the multimedia domain, from the subcategory of audio. " \
                   "Each feature is calculated by analyzing a short-time series of the audio signal using various time-series generated features from the audio signal, " \
                   "obtained by human annotators. " \
                   "The targets represent various aspects of music composition such as the emotional level of the song, the music genre, " \
                   "the instruments present in the recording etc."




d["sameAs"] = ["https://cometa.ujaen.es/datasets/cal500", "http://www.uco.es/kdis/mllresources/#CAL500Desc"]
d["identifier"] = ["https://ieeexplore.ieee.org/document/4432652", "10.1109/TASL.2007.913750"]
d["keywords"] = ["Audio annotation and retrieval", "music information retrieval", "semantic music analysis"]

dd2["name"] = "Douglas Turnbull"
dd2["url"] = "https://scholar.google.com/citations?user=CaEaSR8AAAAJ&hl=en"

dd3["name"] = "Gert Lanckriet"
dd3["url"] = "https://scholar.google.com/citations?user=acmtRMAAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))