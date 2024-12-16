# profesor_rest.py
import os
import requests
import json
import pandas as pd

def profesor_rest(url):
    filet = '../data/profesor_rest.csv'
    cols = ['id', 'prostor_id', 'ime', 'priimek', 'naziv', 'email']
    if os.path.isfile(filet):
        print("Datoteka " + filet + " obstaja, zato se REST ne uporabi.")
        profesor_rest = pd.read_csv(filet, names=cols)
    else:
        print(" Datoteka " + filet + " ne obstaja, zato se REST uporabi.")
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            profesor_rest = pd.DataFrame.from_dict(data['items'])         
        else:
            print("Napaka pri REST prostor:", response.status_code)
        profesor_rest.to_csv(filet, index=False)
    return profesor_rest
	
