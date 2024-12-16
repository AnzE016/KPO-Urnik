# prostor_rest.py
import os
import requests
import json
import pandas as pd

def prostor_rest(url):
    filet = '../data/prostor_rest.csv'
    cols = ['id', 'naziv', 'kapaciteta', 'vrsta']
    if os.path.isfile(filet):
        print("Datoteka " + filet + " obstaja, zato se REST ne uporabi.")
        prostor_rest = pd.read_csv(filet, names=cols)
    else:
        print(" Datoteka " + filet + " ne obstaja, zato se REST uporabi.")
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            prostor_rest = pd.DataFrame.from_dict(data['items'])         
        else:
            print("Napaka pri REST prostor:", response.status_code)
        prostor_rest.to_csv(filet, index=False)
    return prostor_rest
