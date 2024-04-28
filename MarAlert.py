''' IMPORT STANDARD LIBRARIES '''
import feedparser
import requests
import csv
import logging


''' IMPORT 3RD PARTY LIBRARIES '''
from bs4 import BeautifulSoup

''' DEFINE PSEUDO CONSTANTS '''
# Pulls last 50 MARADMINS published
rss_url = 'https://www.marines.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=6&Site=481&max=10&category=14336'

# archive file of previous MARADMINS
maradminArchive = "maradminArchive.txt"

# MARADMIN titles we want to scrape
titlesOfInterest = ["APPROVED SELECTIONS TO STAFF SERGEANT", "OFFICER PROMOTIONS FOR", "1STLT PROMOTIONS FOR", 
                  "APPROVED SELECTIONS TO GUNNERY SERGEANT", "DUTY ASSIGNMENT MERITORIOUS PROMOTIONS"]

#Friends list
csv_file = "maradmin-alert\\contacts.csv"

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

def commanderGrabber(url,friends):


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
    # [FULLLAST, FULLFIRST]

    message = []
    message.append(f"Fuckers are on the rise:%0A{url}%0A")
    for name in commanderPromotionNames:
          if name in friends:
                message.append(f"{name[1],name[0]} is getting promoted!%0A")
    
    if len(message) > 1:
        requests.get(f"https://api.telegram.org/bot6959601616:AAGSrxjkA5BorYMIlgFAWVhgtDc8fbCKfpM/sendMessage?chat_id=@maradmintesting&text={message}")

def gunnyGrabber(url,friends):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    bodyText = (soup.find('div', class_='body-text'))


    text_content = bodyText.get_text(separator='\r\n')

    lines = text_content.split('\n')


    splitMaradmin = []
    maradminLines = []
    maradminNamePairs = []
    cleanedMaradminNamePairs =[]
    maradminNames = []

    for line in lines:
            splitMaradmin.append(line.split())

    for line in splitMaradmin:
            if len(line) >= 4 and len(line) <= 10 and line[0].isalpha() and line[0].isupper() and len(line[0]) > 1 and line[0] != 'NAME':
                    maradminLines.append(line)


    newline = []
    for line in maradminLines:
        maradminNamePairs.append(newline)
        newline = []
        for word in line:
            if word.isalpha():
                    newline.append(word)



    surrnames = ['III', 'II', 'IV', 'V', 'JR', 'SR']
    for i,line in enumerate(maradminNamePairs):
            if len(line) != 4 and len(line) != 2:
                    if len(line) == 6:
                            cleanedMaradminNamePairs.append([line[0],line[2],line[3],line[5]])
                    if len(line) == 5:
                            if line[1] in surrnames and line[3] not in surrnames:
                                    cleanedMaradminNamePairs.append([line[0],line[2],line[3],line[4]])
                            elif line[3] in surrnames and line[1] not in surrnames:
                                cleanedMaradminNamePairs.append([line[0],line[1],line[2],line[4]])
            else:
                cleanedMaradminNamePairs.append(line)



    for line in cleanedMaradminNamePairs:
        if len(line) == 4:
                    name1 = line[0:2]
                    name2 = line[2:5]
                    maradminNames.append([name1[0].upper(),name1[1][0].upper()])
                    maradminNames.append([name2[0].upper(),name2[1][0].upper()])
        else:
                maradminNames.append([line[0].upper(),line[1][0].upper()])

    #modify friends list to [FULLLAST,FI]
    modifiedFriends = []
    for line in friends:
          modifiedFriends.append([line[0],line[1][0]])


    message = []
    message.append(f"Fuckers are on the rise:%0A{url}%0A")
    for name in maradminNames:
          if name in modifiedFriends:
                message.append(f"{name} is getting promoted!%0A")

    if len(message) > 1:
        requests.get(f"https://api.telegram.org/bot6959601616:AAGSrxjkA5BorYMIlgFAWVhgtDc8fbCKfpM/sendMessage?chat_id=@maradmintesting&text={message}")

def ltGrabber(url,friends):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    bodyText = (soup.find('div', class_='body-text'))


    text_content = bodyText.get_text(separator='\r\n')

    lines = text_content.split('\r\n')


    splitMaradmin = []
    maradminLines = []
    maradminNames = []

    for line in lines:
            splitMaradmin.append(line.split())

    for line in splitMaradmin:
        if len(line) >= 4 and len(line) <= 6 and line[0].isalpha() and len(line[0])>1:
            line = line[:len(line)-2]
            maradminLines.append(line)

    for line in maradminLines:
        if len(line) > 2:
            maradminNames.append([line[2].upper(),line[0].upper()])
        else:
            maradminNames.append([line[0].upper(),line[1].upper()])
    
    message = []
    message.append(f"Fuckers are on the rise: {url}")
    for name in maradminNames:
          if name in friends:
                message.append(f"{name} is getting promoted!")

    if len(message) > 1:
        requests.get(f"https://api.telegram.org/bot6959601616:AAGSrxjkA5BorYMIlgFAWVhgtDc8fbCKfpM/sendMessage?chat_id=@maradmintesting&text={message}")



''' LOCAL CLASSES '''
# NONE

''' MAIN ENTRY POINT '''

if __name__ == "__main__":
    ''' Main Script Entry Point '''
    try:
        friends_names = contactsGrabber(csv_file)

        feed = feedparser.parse(rss_url)

        # Set to store names from the RSS feed
        rss_names_set = set()
        names_and_urls = {}
        
        marchive = open(maradminArchive, "r")
        marchiveLst = marchive.read().split("\n")
        marchive.close()
        

        lst =[]
        # Iterate through entries in the feed
        for entry in feed.entries:
            # Check if the entry title contains any of the desired titles
            if any(title in entry.title.upper() for title in titlesOfInterest) and entry.description not in marchiveLst:
                  #lst.append(f"{entry.description}")
                  with open(maradminArchive, 'a') as file:
                        file.write(f"{entry.description}\n")
                  
                  if 'GUNNERY SERGEANT' in entry.title:
                        gunnyGrabber(entry.link,friends_names)
                  elif 'OFFICER PROMOTIONS' in entry.title:
                        commanderGrabber(entry.link,friends_names)
                  elif '1STLT PROMOTIONS' in entry.title:
                        ltGrabber(entry.link,friends_names)
              
    except Exception as err:
        
        logging.critical("\n\nScript Aborted     ", "Exception =     ", err) 


'''
https://api.telegram.org/bot6959601616:AAGSrxjkA5BorYMIlgFAWVhgtDc8fbCKfpM/sendMessage?chat_id=@maradmintesting&text=test

'''