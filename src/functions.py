import os
from pymongo import MongoClient
import requests
import pandas as pd
from pandas.io.json import json_normalize
import folium
import webbrowser
from folium.plugins import HeatMap
from dotenv import load_dotenv
load_dotenv()

def get_offices_locat2(lon, lat): # This function works on POINTS creation (for Mongodb)
    """
    This function creates geopoints for the given longitude and latitude. This function works for Mongodb data
    """
    offices_locat = {
            "type":"Point",
            "coordinates":[lon, lat]
        }
    return offices_locat
print("HOLA")

def capital_search (m):
    """
    This function search for money in the dataframe series. We try to locate key-letters to determine
    the money amount. We are only considering the money ponderated in $. We'll filter amount-wise.
    """
    money = { 
        "$":1, "M":2, "k":3, "K":4, "B":5
    }
    for key, numero in money.items(): 
        if key in m: 
            return m
    return None

def cambiar (col):
    lista = []   
    for e in range(len(df)):
        lista.append(df.geoloc[e])
    return lista

def findNear(lista,rad):
    return list(db.selected.find({
        "geoloc": {
         "$near": {
           "$geometry": lista,
           "$maxDistance": rad,
         }
       }
    }))

def find_by_rad(radious):
    lst =[] 
    for e in range(len(df)):
        num = findNear(lista[e],radious)
        lst.append(len(num))
    return lst            

def features_search(df, type_, keywords):
    """
    This function call Google Places API in order to search specified criteria such as bus stations, restaurants, etc
    """
    output_file = "json"
    radius = "1500"
    lst = []

    for i in range(len(df)):
        coor = df["latitude"][i].astype(str) + ", " + df["longitude"][i].astype(str)
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/"+ output_file +"?location="+coor +"&radius=" +radius+ "&type="+type_+"&keyword="+keywords + "&key="+ PLACES_KEY
        res = requests.get(url)
        data = res.json()
        lst.append(len(data))
    
    return lst      