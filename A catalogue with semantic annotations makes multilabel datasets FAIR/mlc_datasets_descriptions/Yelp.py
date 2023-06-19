from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Yelp"

d["name"] = dataSetName
d["description"] = "Yelp} is dataset from the text domain. " \
                   "It is concerned with the classification of reviews from customers for restaurants into relevant categories. " \
                   "There are two groups of features, star ratings (represented by binary variables) and textual features consisting of unigrams," \
                   " bigrams and trigrams. The textual features are extracted in such a way that after downcasing all the " \
                   "words and removing special characters the unigrams, bigrams and trigrams are extracted and their frequency among" \
                   " reviews is recorded. Only the ones that have their frequency above the threshold of 300 are preserved." \
                   " The labels represent the abstractions the review refers to. The meaning of the label-sets is a multiple " \
                   "of Food, Service, Ambiance, Deals/Discounts, Worthiness."



d["sameAs"] = ["http://mondego.ics.uci.edu/projects/yelp/", "http://www.uco.es/kdis/mllresources/#YelpDesc"]
d["identifier"] = ["http://mondego.ics.uci.edu/projects/yelp/files/technical_report.pdf"]
d["keywords"] = ["Multi-label classification"]

dd2["name"] = "Hitesh Sajnani"
dd2["url"] = "https://scholar.google.com/citations?user=o4gwhssAAAAJ&hl=en"

dd3["name"] = "	Cristina Videira Lopes"
dd3["url"] = "https://www.ics.uci.edu/~lopes/"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))