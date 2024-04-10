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

url = "https://www.marines.mil/News/Messages/Messages-Display/Article/3718870/officer-promotions-for-april-2024-and-projected-officer-promotions-for-may-2024/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
bodyText = (soup.find('div', class_='body-text'))


text_content = bodyText.get_text(separator='\r\n')

lines = text_content.split('\r\n')


splitMaradmin = []
MaradminLines = []
MaradminLastNames = []

for line in lines:
        splitMaradmin.append(line.split())

for line in splitMaradmin:
     if len(line) >= 4 and len(line) <= 6 and line[0].isalpha() and len(line[0])>1 and line[0] != 'Senior':
          line = line[:len(line)-2]
          MaradminLines.append(line)

for name in MaradminLines:
     print(name)
