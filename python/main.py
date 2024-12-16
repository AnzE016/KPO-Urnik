# main.py
# instaliraj pandas, thefuzz, json ...

#!pip install pandas
#!pip install thefuzz
#!pip install json
#**** vključitev knjižnic - Python
import os
import requests
import json
import pandas as pd
from thefuzz import fuzz

#**** vključitev lastnih knjižnic/funkcij - Python
# funkcije za procesiranje ics 
# !!!preveriti ali datoteka url_profesor_calender2023_2024.txt vsebuje vse koledarje za leto 24/25 
from procesiraj_ics import *

from profesor_rest import *
from prostor_rest import *
from predmet_rest import *
from skupina_rest import *


def main():
#REST URL  za profesorje, prostore, predmete in skupine
    url1 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/profesorji"
    url2 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/prostori"
    url3 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/predmeti"
    url4 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/skupine"
    prof_rest_df = profesor_rest(url1)
    pros_rest_df = prostor_rest(url2)   
    pred_rest_df = predmet_rest(url3)
    skup_rest_df = skupina_rest(url4)

# beri+procesiraj ics ali beri csv
    urnik_df = ics_lista(prof_rest_df)
    #urnik_df = pd.read_csv('urnik24.csv')

if __name__ == "__main__":
    print("Procesiranje REST storitev:")
    main()
    print("Zaključek pridobivanja podatkov.")
