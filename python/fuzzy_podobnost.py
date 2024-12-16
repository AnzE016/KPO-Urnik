# fuzzy_podobnost.py
    
import os
import requests
import json
import pandas as pd
from thefuzz import fuzz

from profesor_rest import *
from prostor_rest import *
from predmet_rest import *
from skupina_rest import *

#def fuzzy_podobnost(koledar,baza):
#    return fuzz.ratio(koledar, baza)
#return fuzz.partial_ratio(koledar, baza)

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

def extract_profesor(url):
    #print(profesor.columns)
    start = url.find('---') + 3
    end   = url.find('.ics')
    substring = url[start:end].strip()
    substring = substring.replace("-", " ")
    #print(substring)
    return substring
    
def odstrani_krilate(prof_rest_df):
    prof_rest_df['ime'] = prof_rest_df['ime'].apply(lambda x: x.replace('č', 'c'))
    prof_rest_df['priimek'] = prof_rest_df['priimek'].apply(lambda x: x.replace('č', 'c'))
    prof_rest_df['ime'] = prof_rest_df['ime'].apply(lambda x: x.replace('Č', 'C'))
    prof_rest_df['priimek'] = prof_rest_df['priimek'].apply(lambda x: x.replace('Č', 'C'))
    
    prof_rest_df['ime'] = prof_rest_df['ime'].apply(lambda x: x.replace('ć', 'c'))
    prof_rest_df['priimek'] = prof_rest_df['priimek'].apply(lambda x: x.replace('ć', 'c'))  
    prof_rest_df['ime'] = prof_rest_df['ime'].apply(lambda x: x.replace('Ć', 'C'))
    prof_rest_df['priimek'] = prof_rest_df['priimek'].apply(lambda x: x.replace('Ć', 'C'))

    prof_rest_df['ime'] = prof_rest_df['ime'].apply(lambda x: x.replace('š', 's'))
    prof_rest_df['priimek'] = prof_rest_df['priimek'].apply(lambda x: x.replace('š', 's'))
    prof_rest_df['ime'] = prof_rest_df['ime'].apply(lambda x: x.replace('Š', 'S'))
    prof_rest_df['priimek'] = prof_rest_df['priimek'].apply(lambda x: x.replace('Š', 'S'))

    prof_rest_df['ime'] = prof_rest_df['ime'].apply(lambda x: x.replace('ž', 'z'))
    prof_rest_df['priimek'] = prof_rest_df['priimek'].apply(lambda x: x.replace('ž', 'z'))      
    prof_rest_df['ime'] = prof_rest_df['ime'].apply(lambda x: x.replace('Ž', 'Z'))
    prof_rest_df['priimek'] = prof_rest_df['priimek'].apply(lambda x: x.replace('Ž', 'Z'))
    	    
def main():
# Example usage:
    url1 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/profesorji"
    url2 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/prostori"
    url3 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/predmeti"
    url4 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/skupine"
    prof_rest_df = profesor_rest(url1)
    pros_rest_df = prostor_rest(url2)   
    pred_rest_df = predmet_rest(url3)
    skup_rest_df = skupina_rest(url4)
    file_list = '../data/url_profesor_2024.txt'
    sdf = pd.DataFrame(columns=['max_sim_index', 'no_eq_sim', \
    'ics_name', 'most_simular_name', 'proposed_id'])
    # preprocess
    odstrani_krilate(prof_rest_df)


    if os.path.isfile(file_list):
        nc_source = []
        filet = open(file_list, 'r')
        lines = filet.readlines()
        count = 0
        for line in lines:
            nc_source.append(line.strip()) 
        for l in range(len(nc_source)):
            alfa = extract_profesor(nc_source[l])
            most_similar_id, most_similar_string, max_similarity, equal_similarity = highest_similarity(alfa,prof_rest_df)
            if max_similarity == 100:
                print(f"Max Sim.: {max_similarity}", f"no_equal_sim: {equal_similarity}", \
                alfa,f"Most Similar String: {most_similar_string}", f"ID: {most_similar_id}")
            else:
                print(f"Max Sim.: {max_similarity}", f"no_equal_sim: {equal_similarity}", \
                alfa,f"Most Similar String: {most_similar_string}", f"ID: ??? {most_similar_id}")
            new_row = pd.DataFrame([[max_similarity, equal_similarity, alfa, most_similar_string, \
            most_similar_id]], columns=sdf.columns)
            sdf = pd.concat([sdf, new_row], ignore_index=True)
        # Sort by the first column using its index (0)
        df_sorted = sdf.sort_values(by=sdf.columns[0])
        pd.reset_option('display.max_rows') 
        print(df_sorted.to_string())

if __name__ == "__main__":
    main()






