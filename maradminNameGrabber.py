from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

def read_names_from_csv(csv_file):
    names = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            first_name = row['first_name']
            last_name = row['last_name']
            names.append((first_name.lower(), last_name.lower()))
    return names

csv_file = 'C:\\github\\maradmin-alert\\contacts.csv'

url = "https://www.marines.mil/News/Messages/Messages-Display/Article/3707403/fy24-approved-selections-to-gunnery-sergeant/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
bodyText = (soup.find('div', class_='body-text'))

if bodyText:
        text_content = bodyText.get_text(separator='\r\n')

        lines = text_content.split('\n')

        splitMaradmin = []
        NamesInMaradmin = []

        for line in lines:
                splitMaradmin.append(line.split())
        
        for line in splitMaradmin:
                if len(line) >= 4 and len(line) <= 10 and line[0].isalpha() and line[0].isupper() and len(line[0]) > 1 and line[0] != 'NAME':
                        NamesInMaradmin.append(line)


friendsNames = read_names_from_csv(csv_file)

for name in splitMaradmin:
      for subname in name:
            if subname.lower() in friendsNames.lower():
                  print(subname)

