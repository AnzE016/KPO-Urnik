import os
import requests
import json
import pandas as pd
from thefuzz import fuzz
from ics import Calendar
import pandasql as psql

from profesor_rest import *
from prostor_rest import *
from predmet_rest import *
from skupina_rest import *

from skupina_ics import *
from izvajalec_ics import *
from ucilnica_ics import *

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
         
def mainkun():
    # pridobi REST dataframe
    url1 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/profesorji"
    url2 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/prostori"
    url3 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/predmeti"
    url4 = "https://zgs6evrhembybfa-apexqxa8.adb.eu-frankfurt-1.oraclecloudapps.com/ords/fovcloud/urnik24/skupine"
    
    prof_rest_df = profesor_rest(url1)
    pros_rest_df = prostor_rest(url2)   
    pred_rest_df = predmet_rest(url3)
    skup_rest_df = skupina_rest(url4)
    
    # pridobi vse koledarje skupin, profesorjev in učilnic
    # stringe dobim na https://urnik.fov.um.si/#.... vsi programi, vsi izvajalci, vse učilnice
    cs_skupine = "Koledar: ---3-letnik-UNI-Informacijski-sistemi-Izredni, ---Izberi urnik---, 01---1-letnik-VS-Informacijski-sistemi-Redni, 02---1-letnik-VS-Informacijski-sistemi-Izredni, 03---1-letnik-VS-Kadrovsko-izobrazevalni-sistemi-Redni, 04---1-letnik-VS-Kadrovsko-izobrazevalni-sistemi-Izredni, 05---1-letnik-VS-Inzenirnig-poslovnih-sistemov-Redni, 06---1-letnik-VS-Inzenirnig-poslovnih-sistemov-Izredni, 07---1-letnik-VS-Krizni-management-Izredni, 07---1-letnik-VS-Management-v-sportu-Izredni, 07---2-letnik-VS-Informacijski-sistemi-Redni, 08---2-letnik-VS-Informacijski-sistemi-Izredni, 09---2-letnik-VS-Kadrovsko-izobrazevalni-sistemi-Redni, 10---2-letnik-VS-Kadrovsko-izobrazevalni-sistemi-Izredni, 11---2-letnik-VS-Inzenirnig-poslovnih-sistemov-Redni, 12---2-letnik-VS-Inzenirnig-poslovnih-sistemov-Izredni, 13---2-letnik-VS-Krizni-management-Izredni, 13---2-letnik-VS-Management-v-sportu-Izredni, 13---3-letnik-VS-Informacijski-sistemi-Redni, 14---3-letnik-VS-Informacijski-sistemi-Izredni, 15---3-letnik-VS-Kadrovsko-izobrazevalni-sistemi-Redni, 16---3-letnik-VS-Kadrovsko-izobrazevalni-sistemi-Izredni, 17---3-letnik-VS-Inzenirnig-poslovnih-sistemov-Redni, 18---2-letnik-VS-Management-v-sportu-Izredni, 18---3-letnik-VS-Inzenirnig-poslovnih-sistemov-Izredni, 18---3-letnik-VS-Krizni-management-Izredni, 18---3-letnik-VS-Management-v-sportu-Izredni, 19---1-letnik-UNI-Informacijski-sistemi-Redni, 20---1-letnik-UNI-Informacijski-sistemi-Izredni, 21---1-letnik-UNI-Kadrovsko-izobrazevalni-sistemi-Redni, 22---1-letnik-UNI-Kadrovsko-izobrazevalni-sistemi-Izredni, 23---1-letnik-UNI-Inzenirnig-poslovnih-sistemov-Redni, 24---1-letnik-UNI-Inzenirnig-poslovnih-sistemov-Izredni, 25---2-letnik-UNI-Informacijski-sistemi-Redni, 26---2-letnik-UNI-Informacijski-sistemi-Izredni, 27---2-letnik-UNI-Kadrovsko-izobrazevalni-sistemi-Redni, 28---2-letnik-UNI-Kadrovsko-izobrazevalni-sistemi-Izredni, 29---2-letnik-UNI-Inzenirnig-poslovnih-sistemov-Redni, 30---2-letnik-UNI-Inzenirnig-poslovnih-sistemov-Izredni, 31---3-letnik-UNI-Informacijski-sistemi-Redni, 33---3-letnik-UNI-Kadrovsko-izobrazevalni-sistemi-Redni, 34---3-letnik-UNI-Kadrovsko-izobrazevalni-sistemi-Izredni, 35---3-letnik-UNI-Inzenirnig-poslovnih-sistemov-Redni, 36---3-letnik-UNI-Inzenirnig-poslovnih-sistemov-Izredni, 37---1-letnik-MAG-Informacijski-sistemi-Redni, 38---1-letnik-MAG-Informacijski-sistemi-Izredni, 39---1-letnik-MAG-Kadrovsko-izobrazevalni-sistemi-Redni, 40---1-letnik-MAG-Kadrovsko-izobrazevalni-sistemi-Izredni, 41---1-letnik-MAG-Managament-zdravstva-socialno-varstvo-Redni, 42---1-letnik-MAG-Managament-zdravstva-socialno-varstvo-Izredni, 43---1-letnik-MAG-Inzenirnig-poslovnih-sistemov-Redni, 44---1-letnik-MAG-Inzenirnig-poslovnih-sistemov-Izredni, 45---2-letnik-MAG-Informacijski-sistemi-Redni, 46---2-letnik-MAG-Informacijski-sistemi-Izredni, 47---2-letnik-MAG-Kadrovsko-izobrazevalni-sistemi-Redni, 48---2-letnik-MAG-Kadrovsko-izobrazevalni-sistemi-Izredni, 49---2-letnik-MAG-Managament-zdravstva-socialno-varstvo-Redni, 50---2-letnik-MAG-Managament-zdravstva-socialno-varstvo-Izredni, 51---2-letnik-MAG-Inzenirnig-poslovnih-sistemov-Redni, 52---2-letnik-MAG-Inzenirnig-poslovnih-sistemov-Izredni, 53---1-letnik-DR-Poslovno-delovni-sistemi-Izredni, 54---1-letnik-DR-Kadrovsko-izobrazevalni-sistemi-Izredni, 55---1-letnik-DR-Informacijski-sistemi-Izredni, 56---2-letnik-DR-Poslovno-delovni-sistemi-Izredni, 57---2-letnik-DR-Kadrovsko-izobrazevalni-sistemi-Izredni, 58---2-letnik-DR-Informacijski-sistemi-Izredni"
    cs_profesorji = "Koledar: ---Andreja-Pucihar, ---Izberi urnik---, 01---Bojan-Acko, 01---Olja-Arsenijevic, 02---Alenka-Baggia, 03---Zvone-Balantic, 05---Mojca-Bernik, 06---Bojan-Bostner, 06---Iztok-Bitenc, 06---Stasa-Blatnik, 07---Alenka-Brezavscek, 07---Marina-Dezman, 07---Mojca-Dobnik, 08---Ivan-Erzen, 09---Marko-Ferjan, 10---Albin-Iglicar, 10---Branka-Jarc-Kovacic, 10---Lucija-Gosak, 10---Petra-Robnik, 10---Teodora-Ivanusa, 11---Eva-Jereb, 11---Jana-Krivec, 11---Janja-Jerebic, 12---Spela-Kajzer, 13---Robi-Kelc, 14---Tomaz-Kern, 15---Mirjana-Kljajic-Borstnar, 16---Sandi-Knez, 17---Asistent1, 17---Bojan-Knap, 17---Suzana-Kraljic, 18---Eva-Krhac, 19---Anja-Kozinc, 20---Gregor-Lenart, 21---Andrej-Lisec, 21---Robert-Leskovar, 22---Andreja-Lutar-Skerbinjek, 22---Nevenka-Maher, 23---Damjan-Maletic, 23---Matjaz-Maletic, 24---Blaz-Markelj, 24---Marjeta-Marolt, 24---Miha-Maric, 24---Tilen-Medved, 25---Klemen-Methans, 25---Maja-Mesko, 25---Matjaz-Merc, 25---Sebastjan-Merlo, 26---Dusan-Meznar, 27---Edvard-Kolar, 29---Vesna-Novak, 30---Iztok-Podbregar, 30---Majda-Pajnkihar, 31---Petra-Povalej-Brzan, 31---Rozle-Prezelj, 33---Uros-Rajkovic, 35---Matjaz-Roblek, 36---Urska-Rozman, 37---Gregor-Rus, 37---Marjan-Senegacnik, 38---Andrej-Skraba, 38---Jerneja-Sifrer, 38---Nejc-Celik, 39---Brane-Smitek, 41---Polona-Sprajc, 41---Sonja-Sostar-Turk, 42---Alenka-Tratnik, 42---Gregor-Stiglic, 42---Jadranka-Stricevic, 42---Marina-Stros-Bracko, 42---Mihaela-Stiglic, 43---Ajda-Sulc, 43---Benjamin-Urh, 44---Marko-Urh, 45---Bojan-Vavtar, 45---Bojana-Vasic, 45---Doroteja-Vidmar, 46---Dominika-Vrbnjak, 47---Goran-Vukovic, 48---Borut-Werber, 50---Janez-Zirovnik, 51---Anja-Znidarsic, 52---Jasmina-Znidarsic, 54---Franc-Zeljko-Zupanic, 55---Stefan-Zun, 56---, 56---Asistent-1, 56---Asistent2"
    cs_ucilnice = "Koledar: ---Izberi urnik---, 005, 015, 016, 111, 301, 302, 303, 306, 307, 401, 402, 403, 410, 411, 412, 413"


    # procesiraj skupine - najdi substring '---Izberi urnik---,' 
    start_index = cs_skupine.find('---Izberi urnik---,') + len('---Izberi urnik---,')
    # ekstrahiraj vse za '---Izberi urnik---,'
    ostanek_string = cs_skupine[start_index:]
    # naredi listo l_skupine - skupine so ločene z vejico
    l_skupine = ostanek_string.split(',')
    # izpiši skupine
    #for l in l_skupine:
        #print(l.strip())

    # procesiraj profesorje - najdi substring '---Izberi urnik---,' 
    start_index = cs_profesorji.find('---Izberi urnik---,') + len('---Izberi urnik---,')
    # ekstrahiraj vse za '---Izberi urnik---,'
    ostanek_string = cs_profesorji[start_index:]
    # naredi listo l:profesorji - profesorji so ločeni z vejico
    l_profesorji = ostanek_string.split(',')
    # izpiši podobnosti
    for l in l_profesorji:
        alfa = l[6:len(l)].replace('-',' ')
        most_similar_id, most_similar_string, max_similarity, equal_similarity = highest_similarity(alfa,prof_rest_df)
        print(f"Max Sim.: {max_similarity}", f"no_equal_sim: {equal_similarity}", \
        alfa,f"Most Similar String: {most_similar_string}", f"ID: {most_similar_id}")


    # procesiraj učilnice - najdi substring '---Izberi urnik---,' 
    start_index = cs_ucilnice.find('---Izberi urnik---,') + len('---Izberi urnik---,')
    # ekstrahiraj vse za '---Izberi urnik---,'
    ostanek_string = cs_ucilnice[start_index:]
    # naredi listo l_ucilnice - ucilnice so ločene z vejico
    l_ucilnice = ostanek_string.split(',')

        
    # ekstrahiraj koledarje
    predpona1 = 'https://urnik.fov.um.si/Program/calendars/'
    predpona2 = 'https://urnik.fov.um.si/Izvajalec/calendars/'
    predpona3 = 'https://urnik.fov.um.si/Ucilnica/calendars/'
    
    cal_df_skupine= pd.DataFrame(columns=['skupina', 'dtstamp','dtstart','dtend','trigger','location','description'])
    cal_df_skupine = skupina_ics(l_skupine,predpona1,cal_df_skupine)
    print(cal_df_skupine)
    
    cal_df_profesorji = pd.DataFrame(columns=['profesorji', 'dtstamp','dtstart','dtend','trigger','location','description'])
    cal_df_profesorji = izvajalec_ics(l_profesorji,predpona2,cal_df_profesorji)
    print(cal_df_profesorji)

    cal_df_ucilnice = pd.DataFrame(columns=['lokacije', 'dtstamp','dtstart','dtend','trigger','location','description'])
    cal_df_ucilnice = ucilnica_ics(l_ucilnice,predpona3,cal_df_ucilnice)
    print(cal_df_ucilnice)
    
    # pandas sql
    #query = """
    #SELECT cal_df_skupine.skupina, cal_df_profesorji.profesorji, cal_df_profesorji.dtstart, cal_df_profesorji.location,
    #cal_df_profesorji.description, cal_df_profesorji.trigger, cal_df_profesorji.dtstamp
    #FROM cal_df_skupine
    #LEFT JOIN cal_df_profesorji
    #ON cal_df_skupine.dtstart = cal_df_profesorji.dtstart AND cal_df_skupine.dtend = cal_df_profesorji.dtend  AND
    #cal_df_skupine.location = cal_df_profesorji.location AND cal_df_skupine.description = cal_df_profesorji.description
    #order by cal_df_profesorji.profesorji, cal_df_profesorji.dtstart
    #"""
    
    query = """
    SELECT cal_df_skupine.skupina, cal_df_profesorji.profesorji, cal_df_profesorji.dtstart, cal_df_profesorji.location,
    cal_df_profesorji.description, cal_df_profesorji.dtstamp, cal_df_profesorji.trigger
    FROM cal_df_skupine, cal_df_profesorji, cal_df_ucilnice
    WHERE
    cal_df_skupine.dtstart = cal_df_profesorji.dtstart AND cal_df_skupine.dtend = cal_df_profesorji.dtend  AND
    cal_df_skupine.location = cal_df_profesorji.location AND cal_df_skupine.description = cal_df_profesorji.description AND
    cal_df_skupine.dtstart = cal_df_ucilnice.dtstart AND cal_df_skupine.dtend = cal_df_ucilnice.dtend  AND
    cal_df_skupine.location = cal_df_ucilnice.location AND cal_df_skupine.description = cal_df_ucilnice.description
    order by cal_df_profesorji.location, cal_df_profesorji.profesorji, cal_df_profesorji.dtstart
    """    

    # Execute the query
    result = psql.sqldf(query, locals())

    # Print the result
    print('Število povezanih:', len(result))
    result.to_csv('../data/skupine_profesorji_ucilnice.csv', index=False)

def main():
    try:
        mainkun()
    except Exception as e:
         print(f"An error occurred: {e}")
         import traceback
         traceback.print_exc()
       
if __name__ == "__main__":
    main()
