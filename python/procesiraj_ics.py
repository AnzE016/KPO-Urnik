# procesiraj_ics.py
import os
import requests
from ics import Calendar
#import json
import pandas as pd
#from thefuzz import fuzz

def highest_similarity(par1, par2):
    max_similarity = 0
    most_similar_string = ""
    most_similar_id = None
    equal_similarity = 0
    
    for index, row in par2.iterrows():
        full_name = f"{row['ime']} {row['priimek']}"
        similarity = fuzz.partial_ratio(par1, full_name)
        if similarity == max_similarity:
            equal_similarity = equal_similarity + 1
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_string = full_name
            most_similar_id = row['id']
    
    return most_similar_id, most_similar_string, max_similarity, equal_similarity
    
def ics_lista(prof_rest_df):
    # primer ics_url = 'https://urnik.fov.um.si/Izvajalec/calendars/21---Robert-Leskovar.ics'
    file_list = '../data/url_profesor_2024.txt'
    output_csv= '../data/urnik24.csv' 
    if os.path.isfile(file_list):
        nc_source = []
        filet = open(file_list, 'r')
        lines = filet.readlines()
        count = 0
        for line in lines:
            nc_source.append(line.strip()) 
        for l in range(len(nc_source)):
            # print(l, '. ',nc_source[l], ' ready')
            calendar_df = ics_from_url_to_dataframe(nc_source[l])
            
            calendar_df = calendar_df.replace('Ä', 'č', regex=True)
            calendar_df = calendar_df.replace('Å¡', 'š', regex=True)
            calendar_df = calendar_df.replace('Å¾', 'ž', regex=True)
            calendar_df = calendar_df.replace('Ä', 'ć', regex=True)
            calendar_df = calendar_df.replace('Ä', 'đ', regex=True)

            
            calendar_df = calendar_df.replace('Ä', 'Č', regex=True)
            calendar_df = calendar_df.replace('Ä', 'Ć', regex=True)
            calendar_df = calendar_df.replace('Å ', 'Š', regex=True)
            calendar_df = calendar_df.replace('Å½', 'Ž', regex=True)
            calendar_df = calendar_df.replace('Ä', 'Đ', regex=True)
            #tipkarske napake
            calendar_df = calendar_df.replace('đlovek', 'Človek', regex=True)
            calendar_df = calendar_df.replace('đerne Jan', 'Černe Jan', regex=True)
            calendar_df = calendar_df.replace('đonjić Saša', 'Ćonjić Saša', regex=True)        
        
            if l == 1:
                calendar_df.to_csv(output_csv, mode='w', index=False, header=False)
            else:
                calendar_df.to_csv(output_csv, mode='a', index=False, header=False)
    cols = ['start', 'stop', 'description', 'location', 'name_surname', 'activity', 
            'course_desc', 'location_id', 'prof_id', 'group_id', 'course_id', 'comment', 'URL']
    urnik24 = pd.read_csv('../data/urnik24.csv', names=cols)
    urnik24 = urnik24.drop(1)
    urnik24.to_csv('../data/urnik24.csv', index=False)
    print("Datoteka urnik24.csv pripravljena")
    return calendar_df
    
def ics_from_url_to_dataframe(url):
    # Fetch the .ics file from the URL
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch .ics file from URL: ", url)

    # Parse the .ics content
    c = Calendar(response.text)

    # Extract relevant information from the events in the calendar
    events_data = []
    dogodki = []
    predmeti = []
    for event in c.events:
        event_data = {
            'Start Time': event.begin,
            'End Time': event.end,
            'Summary': event.name,
            #'Description': event.description,
            'Location': event.location
        }
        dogodek = str(event.name)
        dogodki.append(dobi_tip(dogodek)) 
        predmet = dogodek
        predmeti.append(extract_predmet(predmet)) 
        events_data.append(event_data)

    # Convert the events data into a DataFrame
    df = pd.DataFrame(events_data)
    pname = extract_profesor(url)
    #print(dogodki)
    df['Začetek'] = pname
    df['Konec'] = dogodki
    df['Dogodek'] = predmeti
    return df
    
def dobi_tip(dogodek):
    if dogodek[0:7] == 'Zagovor':
        #print('Zagovor')
        return dogodek[0:7]
    elif dogodek[0:7] == 'Konzult':
        #print('Konzultacije')
        start_tipa = index_for_occurrence(dogodek, "-", 2) + 1
        end = start_tipa + 4
        return dogodek[0:12] + ' * ' + dogodek[start_tipa:end]
    elif dogodek[0:4] == 'e-P-':
        #print('e-P-')
        return dogodek[0:3]
    elif dogodek[0:4] == 'e-V-':
         #print('e-V-')
         return dogodek[0:3]
    elif dogodek[0:2] == 'P-':
         #print('P-')
         return dogodek[0:1]
    elif dogodek[0:2] == 'V-':
         #print('V-')
         return dogodek[0:1]

def dobi_predmet(dogodek):
    if dogodek[0:7] == 'Zagovor':
        #print('Zagovor')
        return dogodek[0:7]
    elif dogodek[0:7] == 'Konzult':
        #print('Konzultacije')
        start_predmeta = index_for_occurrence(dogodek, "-", 1) + 1
        start_tipa = index_for_occurrence(dogodek, "-", 2) + 1
        end = start_tipa + 4
        return dogodek[start_predmeta:start_tipa]
    elif dogodek[0:4] == 'e-P-':
        #print('e-P-')
        return dogodek[4:index_for_occurrence(dogodek, "-", 3)]
    elif dogodek[0:4] == 'e-V-':
         #print('e-V-')
        return dogodek[4:index_for_occurrence(dogodek, "-", 3)]
    elif dogodek[0:2] == 'P-':
         #print('P-')
         return dogodek[2:index_for_occurrence(dogodek, "-", 2)]
    elif dogodek[0:2] == 'V-':
         #print('V-')
         return dogodek[2:index_for_occurrence(dogodek, "-", 2)]

    start = url.find('---') + 3
    end   = url.find('.ics')
    substring = url[start:end].strip()
    substring = substring.replace("-", " ")
    #print(substring)
    return substring

def extract_profesor(url):
    #print(profesor.columns)
    start = url.find('---') + 3
    end   = url.find('.ics')
    substring = url[start:end].strip()
    substring = substring.replace("-", " ")
    #print(substring)
    return substring
    
def extract_predmet(dogodek):
    if dogodek[0:7] == 'Zagovor':
        #print('Zagovor')
        return dogodek[0:7]
    elif dogodek[0:7] == 'Konzult':
        #print('Konzultacije')
        start_predmeta = index_for_occurrence(dogodek, "-", 1) + 1
        start_tipa = index_for_occurrence(dogodek, "-", 2) + 1
        end = start_tipa + 4
        return dogodek[start_predmeta:start_tipa]
    elif dogodek[0:4] == 'e-P-':
        #print('e-P-')
        return dogodek[4:index_for_occurrence(dogodek, "-", 3)]
    elif dogodek[0:4] == 'e-V-':
         #print('e-V-')
        return dogodek[4:index_for_occurrence(dogodek, "-", 3)]
    elif dogodek[0:2] == 'P-':
         #print('P-')
         return dogodek[2:index_for_occurrence(dogodek, "-", 2)]
    elif dogodek[0:2] == 'V-':
         #print('V-')
         return dogodek[2:index_for_occurrence(dogodek, "-", 2)]

    start = url.find('---') + 3
    end   = url.find('.ics')
    substring = url[start:end].strip()
    substring = substring.replace("-", " ")
    #print(substring)
    return substring

def index_for_occurrence(text, token, occurrence):
    gen = (i for i, l in enumerate(text) if l == token)
    for _ in range(occurrence - 1):
        next(gen)
    return next(gen)
