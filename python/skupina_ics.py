# skupina_urnik.py

import os
import requests
import json
import pandas as pd
from thefuzz import fuzz
from ics import Calendar
from obdelaj_ics import *

def skupina_ics(l_skupine,predpona1,cal_df_skupine):
    filet = '../data/skupina_ics.csv'
    
    if os.path.isfile(filet):
        print("Datoteka " + filet + " obstaja, zato ics datotek ne procesiramo.")
        cal_df_skupine = pd.read_csv(filet)
    else:
        print(" Datoteka " + filet + " ne obstaja, zato procesirano ics datoteke.")
        for l in range(len(l_skupine)):
            obdelaj_ics(l_skupine[l],predpona1,cal_df_skupine)
        cal_df_skupine.to_csv(filet, index=False)
    return cal_df_skupine
