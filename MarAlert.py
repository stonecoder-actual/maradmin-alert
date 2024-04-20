''' IMPORT STANDARD LIBRARIES '''
import feedparser
import requests
import csv
import logging


''' IMPORT 3RD PARTY LIBRARIES '''
from prettytable import PrettyTable     # pip install prettytable
from bs4 import BeautifulSoup

''' DEFINE PSEUDO CONSTANTS '''
# Pulls last 50 MARADMINS published
#rss_url = 'https://www.marines.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=6&Site=481&max=50&category=14336'
rss_url = "https://www.marines.mil/News/Messages/Messages-Display/Article/3718870/officer-promotions-for-april-2024-and-projected-officer-promotions-for-may-2024/"

# MARADMIN titles we want to scrape
titlesOfInterest = ["APPROVED SELECTIONS TO STAFF SERGEANT", "OFFICER PROMOTIONS FOR", "1STLT PROMOTIONS FOR", 
                  "APPROVED SELECTIONS TO GUNNERY SERGEANT", "DUTY ASSIGNMENT MERITORIOUS PROMOTIONS"]

#Friends list
csv_file = "maradmin-alert\\contacts.csv"

''' LOCAL FUNCTIONS '''

def contactsGrabber(csv):
    friendsNames = []
    with open(csv, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            first_name = row['first_name']
            last_name = row['last_name']
            names.append([last_name.upper(), first_name.upper()])
    # return [FULLLAST, FULLFIRST]
    return friendsNames



def commanderGrabber(url):


    #url = "https://www.marines.mil/News/Messages/Messages-Display/Article/3718870/officer-promotions-for-april-2024-and-projected-officer-promotions-for-may-2024/"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    bodyText = (soup.find('div', class_='body-text'))


    text_content = bodyText.get_text(separator='\r\n')

    lines = text_content.split('\r\n')


    splitMaradmin = []
    maradminLines = []
    commanderPromotionNames = []

    for line in lines:
            splitMaradmin.append(line.split())

    for line in splitMaradmin:
        if len(line) >= 4 and len(line) <= 6 and line[0].isalpha() and len(line[0])>1 and line[0] != 'Senior':
            line = line[:len(line)-2]
            maradminLines.append(line)

    for name in maradminLines:
        if len(name[1]) > 2:
             commanderPromotionNames.append([name[1].upper(),name[0].upper()])
        else:
             commanderPromotionNames.append([name[2].upper(),name[0].upper()])
    return commanderPromotionNames

# return [FULLLAST, FULLFIRST]



















''' LOCAL CLASSES '''
# NONE

''' MAIN ENTRY POINT '''

if __name__ == "__main__":
    ''' Main Script Entry Point '''
    try:
            
            # friends_names = read_names_from_csv(csv_file_path)    
            # monitor_rss_feed(rss_url, maradminTitles, friends_names)
            commanderGrabber(rss_url)


            
        
            
    except Exception as err:
        
        logging.critical("\n\nScript Aborted     ", "Exception =     ", err) 

