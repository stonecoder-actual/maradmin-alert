''' IMPORT STANDARD LIBRARIES '''
import feedparser
import requests
import csv
import logging


''' IMPORT 3RD PARTY LIBRARIES '''
from bs4 import BeautifulSoup

''' DEFINE PSEUDO CONSTANTS '''
alnav25 = "https://www.mynavyhr.navy.mil/Portals/55/Messages/ALNAV/ALN2025/ALN25"

''' LOCAL FUNCTIONS '''

def contactsGrabber(_csv):
    friendsNames = []
    with open(_csv, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            first_name = row['first_name']
            last_name = row['last_name']
            friendsNames.append([last_name.upper(), first_name.upper()])
    # return [FULLLAST, FULLFIRST]
    return friendsNames

''' LOCAL CLASSES '''
# NONE

''' MAIN ENTRY POINT '''

if __name__ == "__main__":
    ''' Main Script Entry Point '''
    try:
    
    
    except Exception as err:
        
        logging.critical("\n\nScript Aborted     ", "Exception =     ", err) 