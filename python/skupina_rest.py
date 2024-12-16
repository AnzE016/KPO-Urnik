# skupina_rest.py
import os
import requests
import json
import pandas as pd
def skupina_rest(url):
    filet = '../data/skupina_rest.csv'
    cols = ["id","naziv"]
    if os.path.isfile(filet):
        print("Datoteka " + filet + " obstaja, zato se REST ne uporabi.")
        skupina_rest = pd.read_csv(filet, names=cols)
    else:
        print(" Datoteka " + filet + " ne obstaja, zato se REST uporabi.")
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            skupina_rest = pd.DataFrame.from_dict(data['items'])         
        else:
            print("Napaka pri REST prostor:", response.status_code)
        skupina_rest.to_csv(filet, index=False)
    return skupina_rest
