from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "EurLex-sm"

d["name"] = dataSetName
d["description"] = "EurLex-sm dataset is a multi-label dataset derived from a freely accessibly repositroy for Eurpoean Union law texts. It includes 19596 documents related to secondary law" \
                   "and international agreements. Regarding the legal form the acts are moslty decisions, regulations, directives and agreements. Each of the document is assigned with several EUROVOC tags. " \
                   "The feature construction and preprocessing is done as follows: the text is extracted from the HTML documents, excluding HTML tags, bibliograpghic notes or other additional information. The text is than" \
                   "tokenized into lower case, stop words are excluded and the porter stemmer algortihm is used. The words are projeted into the vector space model using TF-IDF term weighting. The first 5000 features are selected " \
                   "to reduce the memory requirments. "


d["sameAs"] = ["https://cometa.ujaen.es/datasets/eurlexsm", "http://www.uco.es/kdis/mllresources/#EurlexDesc", "http://mulan.sourceforge.net/datasets-mlc.html"]
d["identifier"] = ["https://link.springer.com/content/pdf/10.1007%2F978-3-540-87481-2_4.pdf", "10.1007/978-3-540-87481-2_4"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Eneldo Loza Mencía"
dd2["url"] = "https://scholar.google.com/citations?user=8Kv6q8wAAAAJ&hl=en"

dd3["name"] = "Johannes Fürnkranz"
dd3["url"] = "https://scholar.google.de/citations?user=sfTn4wEAAAAJ&hl=en"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))