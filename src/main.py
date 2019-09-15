import os
from pymongo import MongoClient
import requests
import pandas as pd
from pandas.io.json import json_normalize
import folium
import webbrowser
from dotenv import load_dotenv
from src.functions import *
load_dotenv()


client = MongoClient('mongodb://localhost:27017/')
db = client.companies

#Starting consuting time on Mongo DB
# We have some criteria when it comes to get the data from our database. The minimums are:
# - There must be some nearby companies that also do design.
# - Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.
# - Developers like to be near successful tech startups with that have raised at least 1 Million dollars.
# - Account managers need to travel a lot
# Therefore, we ask mongodb (politetly) about some of the criteria we are considering.

mongodata = db.companies.find( {"$and":[

                                {"offices.latitude": {"$exists": True}},

                                {"offices.latitude": {"$ne": None}},   

                                {"offices.longitude": {"$exists": True}},

                                {"offices.longitude": {"$ne": None}},

                                {"category_code": {"$exists": True}},

                                {"category_code": {"$ne": None}},   

                                {"founded_year": {"$exists": True}}, 

                                {"founded_year": {"$gte": 2003}},

                                {"deadpooled_year": None},

                                {"number_of_employees": {"$exists": True}},

                                {"total_money_raised": {"$exists": True}},

                                {"total_money_raised":{"$ne":None}},

                                {"total_money_raised": {"$not":{"$size":0}}}, 

                                {"$or": [

                                {"total_money_raised": {"$gte": 1000000}},

                                {"category_code":  "design" } ,

                                {"category_code":  "nanotech" } , 

                                {"category_code":  "web" } , 

                                {"category_code":  "software" } , 

                                {"category_code":  "games_video" } , 

                                {"category_code":  "mobile" } , 

                                {"category_code":  "ecommerce" } ,

                                {"category_code":  "advertising" } ,

                                {"category_code":  "enterprise" } ,   

                                {"category_code":  "analytics" } ,

                                {'category_code':'search'},

                                {'category_code':'network_hosting'} ,   

                                {"category_code":  "photo_video" } ,   

                                {"category_code":  "biotech" } ]} ,

                                ]

                                },

                                {

                               "_id": 0, "category_code": 1,"founded_year": 1, "name": 1, 

                               "offices.country_code": 1, "offices.latitude": 1, "offices.longitude": 1, 

                                "total_money_raised": 1, "number_of_employees":1   

                                }

                            )
# However, the serie "offices" it's a list with embed dicts. 
# The serie contains information about location and number of offices.
# We use json_normalize to extract this information and normalize the serie

df = json_normalize(data = mongodata, record_path = "offices", 
                             meta = ["category_code", "founded_year", "name",
                                    "total_money_raised", "number_of_employees"])
df = df.reindex(columns=['country_code', 'name', 'founded_year', 'category_code', 'latitude', 'longitude', 
                                 'total_money_raised', 'number_of_employees'])

# With this, we create a new column with the number of offices per company.
# As we can see, we have checked that the normalization of the previous column of "offices" has finished properly
df["total_offices"] = df["name"].map(df["name"].value_counts())
df["geoloc"] = df.apply(lambda x: get_offices_locat2(x['longitude'], x['latitude']), axis=1)

# Now, we clean the column number_of_employees to fill NaN values 
df["number_of_employees"].fillna(0, inplace = True)
df["number_of_employees"] =  df["number_of_employees"].fillna(0.0).astype(int)

# Then, we select values on this column above 50, so we filter using this variable (we need to remeber that we are 
# pursuing companies with dynamic teams and lot of activity)
df = df[df["number_of_employees"]>50]

# Also, we have been asked for the value of the company as a condition, therefore:
df = df[df.total_money_raised != "$0"]
df["total_money_raised"] = df["total_money_raised"].apply(capital_search)

# We save it as json file
df.to_json('afines.json', orient="records")

print("We now have our json file ready to be loaded as a new database")


# Let's star working with our new dataset at mongo:

mongodb_selected = db.selected.find()
df = pd.DataFrame(mongodb_selected)
df.dropna(inplace = True)

# With these two functions we aim to transform our geolocation data to list in order to make a geoquery to find how many
# companies we have surrounding each og them in a given radius

lista = cambiar(df, df["geoloc"]) # We apply function "cambiar"

# we now create a list (and then a column) of the number of
# companies close to each of them in 1500 meters


print("Let's filter our dataframe by radious length")

radious_1500 = 1500 # meters

df["nearest_offices"] = find_by_rad(df,lista, radious_1500,)
df_1500 = df.sort_values(by = "nearest_offices", ascending = False)
df_1500.reset_index(inplace=True)
# Let's save our df for 1500 meter  
df_1500.to_csv("for_api_1500.csv")


radious_500 = 500 # meters

df["nearest_offices"] = find_by_rad(df, lista, radious_500)
df_500 = df.sort_values(by = "nearest_offices", ascending = False)
df_500.reset_index(inplace=True)
df_500.to_csv("for_api_500.csv")

radious_2000 = 2000 # meters

df["nearest_offices"] = find_by_rad(df, lista, radious_500)
df_2000 = df.sort_values(by = "nearest_offices", ascending = False)
df_2000.reset_index(inplace=True)
df_2000.to_csv("for_api_2000.csv")

# Now that we have the dataset created, we set our request 
# to Google Maps Api (we are testing with 1500 m output)

print("we set our request to Google Maps Api")
print("We search for car_rentals, restaurants, transit stations and gyms nearby on a 1500 m radious")

df_1500_api = df_1500

df_1500_api["car_rental"] = features_search(df_1500_api, "car_rental", "car+rental")  
df_1500_api["num_restaurants"] = features_search(df_1500_api, "restaurant", "hamburguers")
df_1500_api["buses_stations"] = features_search(df_1500_api, "transit_station", "bus")
df_1500_api["num_gym"] = features_search(df_1500_api, "gym", "gym") 

# We standarize a ranking based on our client demands

df_1500_api["ranking"] = df_1500_api['number_of_employees']*0.8 + df_1500_api['nearest_offices']*0.8 + df_1500_api["num_restaurants"]*0.6 + df_1500_api["car_rental"]*0.5 + df_1500_api["buses_stations"]*0.3 + df_1500_api["num_gym"]*0.3 

my_office = df_1500_api.iloc[df_1500_api['ranking'].argmax()]

coordinates = [ my_office.latitude, my_office.longitude ]
mapa = folium.Map(
        location=coordinates,
        zoom_start=15
    )
folium.Circle(location = coordinates, radius = 500).add_to(mapa)
folium.Marker(coordinates, popup='<b>I should place my office near here!/b>').add_to(mapa)


filepath = '/home/slimbook/git-repos/visualizing-real-world-data/mapa.html'

mapa.save(filepath)

webbrowser.open('file://' + filepath)