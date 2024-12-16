# predmet_rest.py
import os
import requests
import json
import pandas as pd

def predmet_rest(url):
    filet = '../data/predmet_rest.csv'
    cols = ["sifra_predmeta","naziv_predmeta","naziv_programa","strokovni_naziv","stopnja",
            "klasius_srv","klasius_p16","veljavnost_zac","veljavnost_kon","ects","ure_pred",
            "ure_epred","ure_vaj","ure_evaj","ure_labvaj","ind_prof","sam_delo","vrsta_predmeta",
            "id_predmeta","letnik","obv_izb","semester"]
    if os.path.isfile(filet):
        print("Datoteka " + filet + " obstaja, zato se REST ne uporabi.")
        predmet_rest = pd.read_csv(filet, names=cols)
    else:
        print(" Datoteka " + filet + " ne obstaja, zato se REST uporabi.")
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            predmet_rest = pd.DataFrame.from_dict(data['items'])         
        else:
            print("Napaka pri REST prostor:", response.status_code)
        predmet_rest.to_csv(filet, index=False)
    return predmet_rest
