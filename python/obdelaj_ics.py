# obdelaj_ics.py
import os
import requests
import json
import pandas as pd
from thefuzz import fuzz
from ics import Calendar

def obdelaj_ics(lista,tip,cal_df):
    # Fetch the .ics file from the URL
    url = tip + lista.strip() + '.ics'
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Napaka pri branju .ics na URL: ", url)

    # Parse the .ics content
    c = Calendar(response.text)
    for event in c.events:
        description = str(event.name)
        trigger = event.alarms[0].trigger if event.alarms else None
        dtstamp = event.created
        dtstart = event.begin
        dtend = event.end
        location = event.location
        # dodaj novo vrstico v DF
        cal_df.loc[len(cal_df)] = [tip + lista.strip(),dtstamp, dtstart, dtend, trigger, location, description]
