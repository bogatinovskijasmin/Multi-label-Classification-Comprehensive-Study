from pprint import PrettyPrinter
import json

d={}
dd1 = {}
dd2 = {}
dd3 = {}


dataSetName = "Foodtruck"

d["name"] = dataSetName
d["description"] = "Foodtruck is a dataset obtained from a survey conducted with 400 subjects. " \
                   "It represents the personal preferences of the people when ordering food from food trucks.  " \
                   "The attributes represent objective questions about users' profile and their habits and preferences related to food trucks. " \
                   "To use the nominal features they are encoded as one hot vector. " \
                   "Some examples of the features are hygiene, taste, expenses, day period of preference, takeout option, gender, age group etc. " \
                   "The labels are the 12 food types offered: Arabic, fitness, Brazilian, Japanese, gourmet, Mexican, Chinese, healthy, snacks, street, Italian and sweets desserts."



d["sameAs"] = ["https://cometa.ujaen.es/datasets/foodtruck"]
d["identifier"] = ["https://www.researchgate.net/publication/318998885_Food_Truck_Recommendation_Using_Multi-label_Classification", "10.1007/978-3-319-65340-2_48"]
d["keywords"] = ["Food truck recommendation", "Recommendation system", "Multilabel classification", "Multi-label dataset"]

dd2["name"] = "Adriano Rivolli"
dd2["url"] = "https://www.researchgate.net/profile/Adriano_Rivolli"

dd3["name"] = "Andre de Carvalho"
dd3["url"] = "https://www.researchgate.net/profile/Andre_De_Carvalho"

d["creator"] = [dd2, dd3]
p = PrettyPrinter()

with open("/home/jasminb/PycharmProjects/CreateJsonsForDatasets/DescriptionsJsons/" + dataSetName +".json", "w") as file:
    json.dump(d, file)

print(p.pprint(d))